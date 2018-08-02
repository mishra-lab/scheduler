import json
import math
import random
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
from pulp import *

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
        self._var = LpVariable(
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

    def __init__(self, config_path, num_blocks):
        self.config_file = config_path
        self.num_blocks = num_blocks
        self.num_weekends = num_blocks * BLOCK_SIZE
        self.clinicians = {}
        self.divisions = {}
        self.long_weekends = []
        self.problem = LpProblem('scheduler', sense=LpMaximize)
        self.read_config()
        self.setup_solver()

    def setup_solver(self):
        import sys
        if getattr(sys, 'frozen', False):
            # running in a bundle
            cwd = os.getcwd()
            exe = 'cbc-2.9.9-x86\\bin\\cbc.exe'
            solverdir = os.path.join(cwd, exe)
            self.solver = COIN_CMD(path=solverdir)
        else:
            # running from source
            self.solver = LpSolverDefault

    def read_config(self):
        """
        Retrieves static data about clinicians and divisions from a 
        config file.
        """
        with open(self.config_file, 'r') as f:
            data = json.load(f)
            try:
                for clinician in data["CLINICIANS"]:
                    blocks_off, weekends_off = [], []
                    if "blocks_off" in data["CLINICIANS"][clinician]:
                        blocks_off = data["CLINICIANS"][clinician]["blocks_off"]
                    if "weekends_off" in data["CLINICIANS"][clinician]:
                        weekends_off = data["CLINICIANS"][clinician]["weekends_off"]
                    self.clinicians[clinician] = \
                        Clinician(
                            name=clinician,
                            email=data["CLINICIANS"][clinician]["email"],
                            blocks_off=blocks_off,
                            weekends_off=weekends_off)

                for division in data["DIVISIONS"]:
                    self.divisions[division] = Division(division)
                    for clinician in data["DIVISIONS"][division]:
                        self.divisions[division].add_clinician(
                            clinician=self.clinicians[clinician],
                            min_=data["DIVISIONS"][division][clinician]["min"],
                            max_=data["DIVISIONS"][division][clinician]["max"],
                        )

            except KeyError as err:
                print('Invalid config file: missing key {}'.format(str(err)))
                raise err

    def set_timeoff(self, events):
        """
        Populates timeoff for each clinician in self.clinicians based
        on the supplied list of events.
        """
        for event in events:
            start = datetime.strptime(
                event['start'].get('date'),
                '%Y-%m-%d')
            end = datetime.strptime(
                event['end'].get('date'),
                '%Y-%m-%d')
            creator = event['creator'].get('displayName')

            if creator in self.clinicians:
                clinician = self.clinicians[creator]
                # figure out if this time-off request covers a week
                # if not, we can safely ignore it
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

    def set_long_weekends(self, long_weekends):
        """
        Populates set of long weekends (week numbers).
        """
        self.long_weekends = long_weekends

    def build_lp(self):
        """
        Constructs an LP program based on the clinician, division data.
        """
        divisions = list(self.divisions.values())
        clinicians = list(self.clinicians.values())

        self._build_clinician_variables(divisions, clinicians)
        self._build_coverage_constraints(divisions, clinicians)
        self._build_minmax_constraints(divisions)
        self._build_consec_constraints(clinicians)
        self._build_longweekend_constraints(clinicians)
        self._build_adjacency_variables(divisions)
        appeasement_objs = self._build_appeasement_objectives(clinicians)

        self.problem.setObjective(
            (1 / 3) * appeasement_objs[0]
            + (1 / 3) * appeasement_objs[1]
            + (1 / 3) * self._build_adjacency_objective(clinicians)
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
                    lpSum(
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
            self.problem.add(lpSum(
                [_.get_var() for _ in vars_]) == 1)

    def _build_minmax_constraints(self, divisions):
        # mins/maxes per division
        for div in divisions:
            for clinician in div.clinicians:
                (min_, max_) = div.bound_dict[clinician.name]
                sum_ = lpSum(
                    [_.get_var() for _ in div.get_vars_by_name(clinician.name)])
                self.problem.add(sum_ <= max_)
                self.problem.add(sum_ >= min_)

    def _build_consec_constraints(self, clinicians):
        for clinician in clinicians:
            for block_num in range(1, self.num_blocks):
                # if a clinician works a given block, they should not work any
                # adjacent block (even in a different division)
                sum_ = lpSum(
                    [_.get_var() for _ in clinician.get_block_vars(
                        lambda x, block_num=block_num: x.block_num in (block_num, block_num + 1))]
                )
                self.problem.add(sum_ <= 1)

            # at most 1 consecutive weekend of work
            for week_num in range(1, self.num_weekends):
                sum_ = lpSum(
                    [_.get_var() for _ in clinician.get_weekend_vars(
                        lambda x, week_num=week_num: x.week_num in (
                            week_num, week_num + 1)
                    )]
                )
                self.problem.add(sum_ <= 1)

    def _build_longweekend_constraints(self, clinicians):
        if self.long_weekends:
            # equal distribution of long weekends
            max_long_weekends = math.ceil(
                len(self.long_weekends) / len(self.clinicians))
            min_long_weekends = math.floor(
                len(self.long_weekends) / len(self.clinicians))
            for clinician in clinicians:
                sum_ = lpSum(
                    [_.get_var() for _ in clinician.get_weekend_vars(
                        lambda x, l=self.long_weekends: x.week_num in l
                    )]
                )
                self.problem.add(sum_ <= max_long_weekends)
                self.problem.add(sum_ >= min_long_weekends)

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
        return lpSum(adjacency_vars)

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
            lpSum(wa_variables),
            lpSum(ba_variables)
        )

    def solve_lp(self):
        """
        Solves LP program and prints information regarding solution.
        """
        ret = self.problem.solve(self.solver) == LpStatusOptimal
        print('objective value = {}'.format(value(self.problem.objective)))
        print('conflicts per doc:')
        for clinician in self.clinicians.values():
            print(clinician.name)
            assigned_blocksoff = clinician.get_block_vars(
                lambda x, clinician=clinician: x.block_num in clinician.blocks_off and x.get_value() == 1.0)
            assigned_weekendsoff = clinician.get_weekend_vars(
                lambda x, clinician=clinician: x.week_num in clinician.weekends_off and x.get_value() == 1.0)
            print('\t{} out of {} blocks'.format(
                len(assigned_blocksoff), len(clinician.blocks_off)))
            print('\t{} out of {} weekends'.format(
                len(assigned_weekendsoff), len(clinician.weekends_off)))
        print()
        return ret

    def assign_schedule(self):
        """
        Assigns blocks and weekends to clinicians using the results of
        the LP program solution.
        """
        for div in self.divisions.values():
            for block_num in range(1, self.num_blocks + 1):
                assignments = list(filter(lambda x: x.get_value(
                ) == 1.0, div.get_vars_by_block_num(block_num)))
                div.assignments.extend(
                    [_.clinician for _ in assignments]
                )

        for clinician in self.clinicians.values():
            vars_ = clinician.get_weekend_vars(lambda x: x.get_value() == 1.0)
            clinician.weekends_assigned = [_.week_num for _ in vars_]


class API:
    """
    A helper class that wraps some of the API methods of Google calendar.
    """
    SCOPE = 'https://www.googleapis.com/auth/calendar'

    def __init__(self, calendar_id, flags):
        # retrieve credentials / create new
        store = oauth_file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                self.get_client_secret(), API.SCOPE)
            creds = tools.run_flow(flow, store, flags)

        # discover calendar API
        self._service = build(
            'calendar', 'v3', http=creds.authorize(Http()))
        self.calendar_id = calendar_id
        self.time_zone = self.get_timezone()

    def get_client_secret(self):
        import sys
        if getattr(sys, 'frozen', False):
            # running in a bundle
            cwd = os.getcwd()
            file = 'credentials.json'
            return os.path.join(cwd, file)
        else:
            # running from source
            return 'credentials.json'

    def get_timezone(self):
        """
        Returns the timezone of the calendar given by `calendar_id`.
        """
        # pylint: disable=maybe-no-member
        result = self._service.calendars().get(
            calendarId=self.calendar_id).execute()
        return result.get('timeZone')

    def get_events(self, start, end, max_res=1000):
        """
        Returns a list of at most `max_res` events with dates between 
        start and end.
        """
        # pylint: disable=maybe-no-member
        result = self._service.events().list(
            calendarId=self.calendar_id,
            timeMin=start,
            timeMax=end,
            maxResults=max_res,
            singleEvents=True,
            orderBy='startTime').execute()

        return result.get('items', [])

    def create_event(self, start, end, attendees, summary):
        """
        Creates a new event starting at `start` and ending at `end` with
        the given `attendees` and `summary`
        """
        event = {
            'summary': summary,
            'start': {
                'dateTime': start,
                'timeZone': self.time_zone
            },
            'end': {
                'dateTime': end,
                'timeZone': self.time_zone
            },
            'attendees': [
                {'email': _} for _ in attendees
            ]
        }

        # pylint: disable=maybe-no-member
        self._service.events().insert(
            calendarId=self.calendar_id,
            body=event
        ).execute()
