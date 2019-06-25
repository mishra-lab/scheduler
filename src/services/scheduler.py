import json
import math
import os
import random
import sys
from datetime import datetime, timedelta

import pulp
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client import file as oauth_file
from oauth2client import tools

from constants import *


class Variable:
    """
    General LP variable.

    Attributes:
        name (str): The name of the variable
        min (float): The minimum value that the variable can take
        max (float): The maximum value that the variable can take
    """

    def __init__(self, name, min_, max_):
        self.name = name
        self.min = min_
        self.max = max_

        self._init_var()

    def _init_var(self):
        self._var = pulp.LpVariable(
            self.name, lowBound=self.min, upBound=self.max, cat="Integer"
        )

    def get_var(self):
        """
        Returns:
            The underlying `pulp` variable.
        """
        return self._var

    def get_value(self):
        """
        Returns:
            The value of the variable.
        """
        return self._var.varValue


class WeekendVariable(Variable):
    """
    Represents a 0-1 ILP variable corresponding to an assignment between 
    a given clinician and a weekend.

    Attributes:
        clinician (Clinician): The clinician corresponding to this weekend assignment
        week_num (int): The week number corresponding to this weekend assignment
    """

    def __init__(self, clinician, week_num):
        self.clinician = clinician
        self.week_num = week_num

        Variable.__init__(self, '{},weekend:{}'.format(
            self.clinician.name, self.week_num
        ), 0, 1)


class BlockVariable(Variable):
    """
    Represents a 0-1 ILP variable corresponding to an assignment between
    a given clinician and a block of length `BLOCKS_SIZE` for a given
    division.

    Attributes:
        clinician (Clinician): The clinician corresponding to this block assignment
        block_num (int): The block number corresponding to this block assignment
        division (Division): The division corresponding to this block assignment
    """

    def __init__(self, clinician, block_num, division):
        self.clinician = clinician
        self.block_num = block_num
        self.division = division

        Variable.__init__(self, '{},div:{},block:{}'.format(
            self.clinician.name, self.division, self.block_num
        ), 0, 1)


class Division:
    """
    Represents a given division comprised of multiple clinicians.

    Attributes:
        name (str): The name of the division
        clinicians (list): A list of `Clinician` objects that are covering this division
        bound_dict (dict): A dictionary mapping each clinician to a tuple (min, max)
            that represents the bounds on the number of blocks they can be assigned to
        assignments (list): A list of `Clinician` objects where the index corresponds to
            the block number of the assignment
    """

    def __init__(self, name):
        self.name = name
        self.clinicians = []
        self.bound_dict = dict()

        self.assignments = []

    def add_clinician(self, clinician, min_, max_):
        """
        Adds a clinician to this division with block assignment  bounds 
        `min_` and `max_`.
        """
        if clinician not in self.clinicians:
            self.clinicians.append(clinician)
            self.bound_dict[clinician.name] = (min_, max_)

    def remove_clinician(self, clinician):
        """
        Removes an existing clinician from this division.
        """
        if clinician in self.clinicians:
            del self.bound_dict[clinician.name]
            self.clinicians.remove(clinician)

    def reset(self):
        """
        Resets division to pre-solving state
        """
        self.assignments = []

    def get_vars(self):
        """
        Returns all block variables corresponding to this division, across all
        clinicians.
        """
        block_vars = [
            _ for clinician in self.clinicians for _ in clinician.get_block_vars()]
        return list(filter(lambda x: x.division == self.name, block_vars))

    def get_vars_by_block_num(self, block_num):
        """
        Returns all block variables corresponding to this division, across all
        clinicians whose block number is equal to `block_num`.
        """
        return list(filter(lambda x: x.block_num == block_num, self.get_vars()))

    def get_vars_by_name(self, name):
        """
        Returns all block variables corresponding to this division with
        a clinician whose name is equal to `name`.
        """
        return list(filter(lambda x: x.clinician.name == name, self.get_vars()))


class Clinician:
    """
    Stores data regarding a given clinician.
    """

    def __init__(self, name, email, blocks_off=[], weekends_off=[]):
        self.name = name
        self.email = email
        self.blocks_off = blocks_off
        self.weekends_off = weekends_off
        self.weekends_assigned = []

        self._vars = []

    def add_var(self, var):
        """
        Adds a new LP variable to this clinician.
        """
        if var not in self._vars:
            self._vars.append(var)

    def remove_var(self, var):
        """
        Removes an existing LP variable from this clinician.
        """
        if var in self._vars:
            self._vars.remove(var)

    def reset(self):
        """
        Resets clinician to pre-solving state
        """
        self._vars = []
        self.weekends_assigned = []

    def get_vars(self, predicate=None):
        """
        Returns a list of all variables from this clinician that satisfy
        the supplied predicate.
        """
        return list(filter(predicate, self._vars))

    def get_block_vars(self, predicate=None):
        """
        Returns a list of all block variables from this clinician that
        satisfy the supplied predicate.
        """
        return list(filter(predicate, self.get_vars(lambda x: type(x) is BlockVariable)))

    def get_weekend_vars(self, predicate=None):
        """
        Returns a list of all weekend variables from this clinician that
        satisfy the supplied predicate.
        """
        return list(filter(predicate, self.get_vars(lambda x: type(x) is WeekendVariable)))


class Scheduler:
    """
    Implements a scheduling algorithm using LP in order to create a fair
    schedule based on the supplied clinician and division data.
    """

    def __init__(self, logger, num_blocks, clin_data={}, timeoff_data=[], long_weekends=[]):
        self.num_blocks = num_blocks
        self.num_weekends = num_blocks * BLOCK_SIZE

        self.clinicians = {}
        self.divisions = {}
        self.holiday_map = {}
        self.long_weekends = []
        self._logger = logger
        
        self.set_long_weekends(long_weekends)
        self.set_data(clin_data)
        self.set_timeoff(timeoff_data)

    def generate(self, debug=False, shuffle=False):
        self.setup_solver()
        self.setup_problem(shuffle=shuffle)
        ret = self.problem.solve(self.solver) == pulp.LpStatusOptimal
                    
        if ret:
            if debug:
                self._logger.write_line('Objective function value: {}'.format(pulp.value(self.problem.objective)))
                conflicts_str = 'Schedule Conflicts:'
                for clinician in self.clinicians.values():
                    assigned_blocksoff = clinician.get_block_vars(
                        lambda x, clinician=clinician: x.block_num in clinician.blocks_off and x.get_value() == 1.0)
                    assigned_weekendsoff = clinician.get_weekend_vars(
                        lambda x, clinician=clinician: x.week_num in clinician.weekends_off and x.get_value() == 1.0)
                    
                    conflicts_str += ' {0} ({1}/{2} blocks, {3}/{4} weekends)'.format(
                        clinician.name, len(assigned_blocksoff), len(clinician.blocks_off),
                        len(assigned_weekendsoff), len(clinician.weekends_off)
                    )
                self._logger.write_line(conflicts_str)

            self.assign_schedule()
            # only keep assignments mapping
            divAssignments = dict.fromkeys(self.divisions.keys())
            for key in self.divisions.keys():
                div = self.divisions[key]
                divAssignments[key] = [clin.name for clin in div.assignments]

            weekendAssignments = [None] * self.num_weekends
            for clinician in self.clinicians.values():
                for week_num in clinician.weekends_assigned:
                    i = week_num - 1
                    weekendAssignments[i] = clinician.name

            return (divAssignments, weekendAssignments, self.holiday_map)

    def setup_solver(self):
        if getattr(sys, 'frozen', False):
            # running in a bundle
            cwd = os.getcwd()
            exe = 'cbc\\bin\\cbc.exe'
            if hasattr(sys, '_MEIPASS'): solverdir = os.path.join(sys._MEIPASS, exe)
            else: solverdir = exe
            self.solver = pulp.COIN_CMD(path=solverdir)
        else:
            # running from source
            self.solver = pulp.LpSolverDefault

    def set_data(self, data):
        """
        Converts data to a form useable by LP solver
        """
        self.clinicians = {}
        self.divisions = {}

        for clin_name in data:
            clin_object = data[clin_name]

            # populate blocks/weekends off
            blocks_off, weekends_off = [], []
            if 'blocks_off' in clin_object:
                blocks_off = clin_object['blocks_off']
            if 'weekends_off' in clin_object:
                blocks_off = clin_object['weekends_off']

            clinician = Clinician(
                name=clin_name,
                email=clin_object['email'],
                blocks_off=blocks_off,
                weekends_off=weekends_off
            )
            # save to local dict
            self.clinicians[clin_name] = clinician

            # parse divisions
            for div_name in clin_object['divisions']:
                div_object = clin_object['divisions'][div_name]
                # create division in local dict, if necessary
                if div_name not in self.divisions:
                    self.divisions[div_name] = Division(div_name)

                # save to local dict
                self.divisions[div_name].add_clinician(
                    clinician=clinician,
                    min_=div_object['min'],
                    max_=div_object['max']
                )

    def read_config(self, config_path):
        """
        Retrieves static data about clinicians and divisions from a 
        config file.
        """
        with open(config_path, 'r') as f:
            data = json.load(f)
            self.set_data(data)

    def set_timeoff(self, events):
        """
        Populates timeoff for each clinician in self.clinicians based
        on the supplied list of events.
        """
        for event in events:
            start = datetime.strptime(
                event['start'].get('date'),
                '%Y-%m-%d'
            )
            end = datetime.strptime(
                event['end'].get('date'),
                '%Y-%m-%d'
            )
            # creator = event['creator'].get('displayName')
            creator = event['summary'].replace('[request] ', '')

            if creator in self.clinicians:
                clinician = self.clinicians[creator]
                # figure out whether this timeoff request intersects a 
                # week or a weekend
                weeks = []
                weekends = []
                curr = start
                while curr < end:
                    week_num = curr.isocalendar()[1]
                    if curr.isoweekday() in range(1, 6):
                        if week_num not in weeks:
                            weeks.append(week_num)
                    else:
                        if week_num not in weekends:
                            weekends.append(week_num)

                    curr += timedelta(days=1)

                for week_num in weeks:
                    block_num = math.ceil(week_num / BLOCK_SIZE)
                    if block_num not in clinician.blocks_off:
                        clinician.blocks_off.append(block_num)
                for week_num in weekends:
                    if week_num not in clinician.weekends_off:
                        clinician.weekends_off.append(week_num)
            else:
                print('Event creator {} was not found in clinicians'.format(creator))

    def set_long_weekends(self, events):
        lw = dict()
        for event in events:
            start = datetime.strptime(
                event['start'].get('date'),
                '%Y-%m-%d'
            )

            # Fri statutory holidays are associated with their regular weeknum
            # Mon statutory holidays are associated with their weeknum - 1
            #   (i.e.: the previous weeknum)
            if start.isoweekday() == 1:
                lw[event['start']['date']] = start.isocalendar()[1] - 1
                # lw.add(start.isocalendar()[1] - 1)
            elif start.isoweekday() == 5:
                lw[event['start']['date']] = start.isocalendar()[1]
                # lw.add(start.isocalendar()[1])

        self.holiday_map = lw
        self.long_weekends = list(lw.values())
    
    def setup_problem(self, shuffle=False):
        """
        Constructs an LP program based on the clinician, division data.
        """
        self.problem = pulp.LpProblem('scheduler', sense=pulp.LpMaximize)

        for clinician in self.clinicians.values(): clinician.reset()
        for division in self.divisions.values(): division.reset()

        divisions = list(self.divisions.values())
        clinicians = list(self.clinicians.values())

        if shuffle: random.shuffle(clinicians)

        self._build_clinician_variables(divisions, clinicians)
        self._build_coverage_constraints(divisions, clinicians)
        self._build_minmax_constraints(divisions)
        self._build_consec_constraints(clinicians)
        self._build_spread_constraints(clinicians)
        self._build_longweekend_constraints(clinicians)
        self._build_weekend_constraints(clinicians)
        self._build_adjacency_variables(divisions)
        appeasement_objs = self._build_appeasement_objectives(clinicians)

        num_clin = len(clinicians)
        num_div = len(divisions)

        # make sure to normalize objectives, and weigh them equally
        self.problem.setObjective(
              (1 / 3) * (1 / (num_clin * self.num_blocks * num_div)) * appeasement_objs[0]
            + (1 / 3) * (1 / (num_clin * self.num_weekends)) * appeasement_objs[1]
            + (1 / 3) * (1 / (num_clin * self.num_blocks * num_div)) * self._build_adjacency_objective(clinicians)
        )

    def _build_clinician_variables(self, divisions, clinicians):
        # create clinician BlockVariables
        for div in divisions:
            for clinician in div.clinicians:
                for block_num in range(1, self.num_blocks + 1):
                    clinician.add_var(
                        BlockVariable(clinician, block_num,
                                      div.name)
                    )
        # create clinician WeekendVariables
        for clinician in clinicians:
            for week_num in range(1, self.num_weekends + 1):
                clinician.add_var(
                    WeekendVariable(clinician, week_num)
                )

    def _build_coverage_constraints(self, divisions, clinicians):
        # no holes + no overlap over all divisions (BLOCKS)
        for div in divisions:
            for block_num in range(1, self.num_blocks + 1):
                self.problem.add(
                    pulp.lpSum(
                        [_.get_var()
                         for _ in div.get_vars_by_block_num(block_num)]
                    ) == 1
                )

        # no holes + no overlap (WEEKENDS)
        for week_num in range(1, self.num_weekends + 1):
            vars_ = \
                [_ for clinician in clinicians
                    for _ in clinician.get_weekend_vars(
                        lambda x, week_num=week_num: x.week_num == week_num
                    )
                 ]
            self.problem.add(pulp.lpSum(
                [_.get_var() for _ in vars_]) == 1)

    def _build_minmax_constraints(self, divisions):
        # mins/maxes per division
        for div in divisions:
            for clinician in div.clinicians:
                (min_, max_) = div.bound_dict[clinician.name]
                sum_ = pulp.lpSum(
                    [_.get_var() for _ in div.get_vars_by_name(clinician.name)])
                self.problem.add(sum_ <= max_)
                self.problem.add(sum_ >= min_)

    def _build_consec_constraints(self, clinicians):
        for clinician in clinicians:
            for block_num in range(1, self.num_blocks):
                # if a clinician works a given block, they should not work any
                # adjacent block (even in a different division)
                sum_ = pulp.lpSum(
                    [_.get_var() for _ in clinician.get_block_vars(
                        lambda x, block_num=block_num: x.block_num in (block_num, block_num + 1))]
                )
                self.problem.add(sum_ <= 1)

            # at most 1 consecutive weekend of work
            for week_num in range(1, self.num_weekends):
                sum_ = pulp.lpSum(
                    [_.get_var() for _ in clinician.get_weekend_vars(
                        lambda x, week_num=week_num: x.week_num in (
                            week_num, week_num + 1)
                    )]
                )
                self.problem.add(sum_ <= 1)

    def _build_spread_constraints(self, clinicians):
        # we need at least 5 consecutive blocks to implement this constraint
        # on-off-on-off-on
        if self.num_blocks <= 5: return

        for clinician in clinicians:
            for block_num in range(1, self.num_blocks - 3):
                # constraint: X_i + X_{i+2} + X_{i+4} <= 2
                sum_ = pulp.lpSum(
                    [_.get_var() for _ in clinician.get_block_vars(
                        lambda x, block_num=block_num: x.block_num in (block_num, block_num + 2, block_num + 4))]
                )
                self.problem.add(sum_ <= 2)

    def _build_longweekend_constraints(self, clinicians):
        if self.long_weekends:
            # (roughly) equal distribution of long weekends
            max_long_weekends = math.ceil(
                len(self.long_weekends) / len(self.clinicians))
            min_long_weekends = math.floor(
                len(self.long_weekends) / len(self.clinicians))
            for clinician in clinicians:
                sum_ = pulp.lpSum(
                    [_.get_var() for _ in clinician.get_weekend_vars(
                        lambda x, l=self.long_weekends: x.week_num in l
                    )]
                )
                self.problem.add(sum_ <= max_long_weekends)
                self.problem.add(sum_ >= min_long_weekends)

    def _build_weekend_constraints(self, clinicians):
        # (roughly) equal distribution of weekends
        max_weekends = math.ceil(
            self.num_weekends / len(clinicians)
        )
        min_weekends = math.floor(
            self.num_weekends / len(clinicians)
        )

        for clinician in clinicians:
            sum_ = pulp.lpSum(
                [_.get_var() for _ in clinician.get_weekend_vars()]
            )
            self.problem.add(sum_ <= max_weekends)
            self.problem.add(sum_ >= min_weekends)

    def _build_adjacency_variables(self, divisions):
        # block-adjacent weekends
        # -----------------------
        # for each pair (block_num, week_num) where
        #   week_num = block_num * BLOCK_SIZE - 1
        # we define a helper variable, used to maximize the product:
        #   BlockVariable[block_num] * WeekendVariable[week_num]
        # moreover, we constrain the helper variable to be at most
        # BlockVariable[block_num] and WeekendVariable[week_num]
        #
        # note: maximizing a product of variables is NOT a linear program
        # which is precisely why we need a helper variable.
        for div in divisions:
            for clinician in div.clinicians:
                for block_num in range(1, self.num_blocks + 1):
                    week_num = block_num * BLOCK_SIZE - 1

                    block_var = clinician.get_block_vars(
                        lambda x, d=div.name, b=block_num:
                            x.block_num == b and
                            x.division == d
                    )[0].get_var()
                    weekend_var = clinician.get_weekend_vars(
                        lambda x, w=week_num: x.week_num == w)[0].get_var()

                    var_ = Variable(
                        '{}:adjacency,div:{},block:{}*weekend:{}'.format(
                            clinician.name,
                            div.name,
                            block_num,
                            week_num
                        ),
                        0, 1)
                    clinician.add_var(var_)
                    self.problem.add(var_.get_var() <= block_var)
                    self.problem.add(var_.get_var() <= weekend_var)

    def _build_adjacency_objective(self, clinicians):
        adjacency_vars = []
        for clinician in clinicians:
            adjacency_vars.extend(
                [_.get_var() for _ in clinician.get_vars(
                    lambda x: 'adjacency' in x.name
                )]
            )
        return pulp.lpSum(adjacency_vars)

    def _build_appeasement_objectives(self, clinicians):
        wa_variables = []
        for clinician in clinicians:
            wa_variables.extend(
                [_.get_var() for _ in clinician.get_weekend_vars(
                    lambda x, clinician=clinician: x.week_num not in clinician.weekends_off)
                 ]
            )

            wa_variables.extend(
                [-_.get_var() for _ in clinician.get_weekend_vars(
                    lambda x, clinician=clinician: x.week_num in clinician.weekends_off)
                 ]
            )

        ba_variables = []
        for clinician in clinicians:
            ba_variables.extend(
                [_.get_var() for _ in clinician.get_block_vars(
                    lambda x, clinician=clinician: x.block_num not in clinician.blocks_off)
                 ]
            )

            ba_variables.extend(
                [-_.get_var() for _ in clinician.get_block_vars(
                    lambda x, clinician=clinician: x.block_num in clinician.blocks_off)
                 ]
            )

        return (
            pulp.lpSum(wa_variables),
            pulp.lpSum(ba_variables)
        )

    def assign_schedule(self):
        """
        Assigns blocks and weekends to clinicians using the results of
        the LP program solution.
        """
        for div in self.divisions.values():
            for block_num in range(1, self.num_blocks + 1):
                assignments = list(filter(lambda x: x.get_value(
                ) == 1.0, div.get_vars_by_block_num(block_num)))

                for _ in range(BLOCK_SIZE):
                    div.assignments.extend(
                        [__.clinician for __ in assignments]
                    )

        for clinician in self.clinicians.values():
            vars_ = clinician.get_weekend_vars(lambda x: x.get_value() == 1.0)
            clinician.weekends_assigned = [_.week_num for _ in vars_]
