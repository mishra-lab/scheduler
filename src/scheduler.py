import json
import math
import random
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from ortools.linear_solver import pywraplp

NUM_BLOCKS = 26
# mon 8am + 105 hours = fri 5pm
# 105 = 4 * 24hr + (17hr - 8hr)
WEEK_HOURS = 24 * 4 + (17 - 8)

# fri 5pm + 63 hours = mon 8am
WEEKEND_HOURS = 24 * 2 + 24 - (17 - 8)

BLOCK_SIZE = 2

NUM_WEEKENDS = BLOCK_SIZE * NUM_BLOCKS


class Variable:
    """
    General LP variable.

    Attributes:
        name (str): The name of the variable
        min (float): The minimum value that the variable can take
        max (float): The maximum value that the variable can take
    """

    def __init__(self, name, min_, max_, solver):
        self.name = name
        self.min = min_
        self.max = max_

        self._init_var(solver)

    def _init_var(self, solver):
        # register variable in LP solver
        self._var = solver.IntVar(
            self.min, self.max, self.name
        )

    def get_var(self):
        """
        Returns:
            The underlying `pywraplp` variable.
        """
        return self._var

    def get_value(self):
        """
        Returns:
            The value of the variable.
        """
        return self._var.solution_value()


class WeekendVariable(Variable):
    """
    Represents a 0-1 ILP variable corresponding to an assignment between 
    a given clinician and a weekend.

    Attributes:
        clinician (Clinician): The clinician corresponding to this weekend assignment
        week_num (int): The week number corresponding to this weekend assignment
    """

    def __init__(self, clinician, week_num, solver):
        self.clinician = clinician
        self.week_num = week_num

        Variable.__init__(self, '{},weekend:{}'.format(
            self.clinician.name, self.week_num
        ), 0, 1, solver)


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

    def __init__(self, clinician, block_num, division, solver):
        self.clinician = clinician
        self.block_num = block_num
        self.division = division

        Variable.__init__(self, '{},div:{},block:{}'.format(
            self.clinician.name, self.division, self.block_num
        ), 0, 1, solver)


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

    def __init__(self, settings):
        secret_path = '../config/client_secret.json'
        calendar_id = 'primary'

        secret_path = settings.get_path_from_key('secret_path')
        calendar_id = settings['calendar_id']
        self.config_file = settings.get_path_from_key('clinician_config_path')

        self._API = API(secret_path, calendar_id, settings)
        self.clinicians = {}
        self.divisions = {}
        self.long_weekends = []
        self.solver = pywraplp.Solver(
            'scheduler', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    def read_config(self):
        """
        Retrieves static data about clinicians and divisions from a 
        config file.
        """
        with open(self.config_file, 'r') as f:
            data = json.load(f)
            try:
                for clinician in data["CLINICIANS"]:
                    self.clinicians[clinician] = \
                        Clinician(
                            name=clinician,
                            email=data["CLINICIANS"][clinician]["email"],
                            blocks_off=data["CLINICIANS"][clinician]["blocks_off"],
                            weekends_off=data["CLINICIANS"][clinician]["weekends_off"])

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

    def read_timeoff(self):
        """
        Retrieves timeoff events for each clinician in self.clinicians
        from Google calendar.
        """
        now = datetime.utcnow().isoformat() + 'Z'
        events = self._API.get_events(start=now)

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

    def read_long_weekends(self):
        """
        Retrieves set of long weekends (week numbers) from Google calendar.
        """
        # TODO: Implement!
        raise NotImplementedError()

    def build_lp(self):
        """
        Constructs an LP program based on the clinician, division data.
        """
        divisions = list(self.divisions.values())
        clinicians = list(self.clinicians.values())

        # random.shuffle(divisions)
        # random.shuffle(clinicians)

        self._build_clinician_variables(divisions, clinicians)
        self._build_coverage_constraints(divisions, clinicians)
        self._build_minmax_constraints(divisions)
        self._build_consec_constraints(clinicians)
        self._build_longweekend_constraints(clinicians)
        self._build_adjacency_variables(divisions)
        appeasement_objs = self._build_appeasement_objectives(clinicians)

        self.solver.Maximize(
              (1/3) * appeasement_objs[0]
            + (1/3) * appeasement_objs[1]
            + (1/3) * self._build_adjacency_objective(clinicians)
        )

    def _build_clinician_variables(self, divisions, clinicians):
        # create clinician BlockVariables
        for div in divisions:
            for clinician in div.clinicians:
                for block_num in range(1, NUM_BLOCKS + 1):
                    clinician.add_var(
                        BlockVariable(clinician, block_num,
                                      div.name, self.solver)
                    )
        # create clinician WeekendVariables
        for clinician in clinicians:
            for week_num in range(1, NUM_WEEKENDS + 1):
                clinician.add_var(
                    WeekendVariable(clinician, week_num, self.solver)
                )

    def _build_coverage_constraints(self, divisions, clinicians):
        # no holes + no overlap over all divisions (BLOCKS)
        for div in divisions:
            for block_num in range(1, NUM_BLOCKS + 1):
                self.solver.Add(
                    self.solver.Sum(
                        [_.get_var()
                         for _ in div.get_vars_by_block_num(block_num)]
                    ) == 1
                )

        # no holes + no overlap (WEEKENDS)
        for week_num in range(1, NUM_WEEKENDS + 1):
            vars_ = \
                [_ for clinician in clinicians
                    for _ in clinician.get_weekend_vars(
                        lambda x, week_num=week_num: x.week_num == week_num
                )
                ]
            self.solver.Add(self.solver.Sum(
                [_.get_var() for _ in vars_]) == 1)

    def _build_minmax_constraints(self, divisions):
        # mins/maxes per division
        for div in divisions:
            for clinician in div.clinicians:
                (min_, max_) = div.bound_dict[clinician.name]
                sum_ = self.solver.Sum(
                    [_.get_var() for _ in div.get_vars_by_name(clinician.name)])
                self.solver.Add(sum_ <= max_)
                self.solver.Add(sum_ >= min_)

    def _build_consec_constraints(self, clinicians):
        for clinician in clinicians:
            for block_num in range(1, NUM_BLOCKS):
                # if a clinician works a given block, they should not work any
                # adjacent block (even in a different division)
                sum_ = self.solver.Sum(
                    [_.get_var() for _ in clinician.get_block_vars(
                        lambda x, block_num=block_num: x.block_num in (block_num, block_num + 1))]
                )
                self.solver.Add(sum_ <= 1)

            # at most 1 consecutive weekend of work
            for week_num in range(1, NUM_WEEKENDS):
                sum_ = self.solver.Sum(
                    [_.get_var() for _ in clinician.get_weekend_vars(
                        lambda x, week_num=week_num: x.week_num in (
                            week_num, week_num + 1)
                    )]
                )
                self.solver.Add(sum_ <= 1)

    def _build_longweekend_constraints(self, clinicians):
        # equal distribution of long weekends
        max_long_weekends = math.ceil(
            len(self.long_weekends) / len(self.clinicians))
        min_long_weekends = math.floor(
            len(self.long_weekends) / len(self.clinicians))
        for clinician in clinicians:
            sum_ = self.solver.Sum(
                [_.get_var() for _ in clinician.get_weekend_vars(
                    lambda x, l=self.long_weekends: x.week_num in l
                )]
            )
            self.solver.Add(sum_ <= max_long_weekends)
            self.solver.Add(sum_ >= min_long_weekends)

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
        # for div in self.divisions.values():
        for div in divisions:
            for clinician in div.clinicians:
                for block_num in range(1, NUM_BLOCKS + 1):
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
                        0, 1, self.solver)
                    clinician.add_var(var_)
                    self.solver.Add(var_.get_var() <= block_var)
                    self.solver.Add(var_.get_var() <= weekend_var)

    def _build_adjacency_objective(self, clinicians):
        adjacency_vars = []
        for clinician in clinicians:
            adjacency_vars.extend(
                [_.get_var() for _ in clinician.get_vars(
                    lambda x: 'adjacency' in x.name
                )]
            )
        return self.solver.Sum(adjacency_vars)

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
        weekend_appeasement_count = self.solver.Sum(wa_variables)

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
            self.solver.Sum(wa_variables),
            self.solver.Sum(ba_variables)
        )

    def solve_lp(self):
        """
        Solves LP program and prints information regarding solution.
        """
        ret = self.solver.Solve() == self.solver.OPTIMAL
        print('objective value = {}'.format(self.solver.Objective().Value()))
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
            for block_num in range(1, NUM_BLOCKS + 1):
                assignments = list(filter(lambda x: x.get_value(
                ) == 1.0, div.get_vars_by_block_num(block_num)))
                div.assignments.extend(
                    [_.clinician for _ in assignments]
                )

        for clinician in self.clinicians.values():
            vars_ = clinician.get_weekend_vars(lambda x: x.get_value() == 1.0)
            clinician.weekends_assigned = [_.week_num for _ in vars_]

    def publish_schedule(self):
        """
        Publishes the block and weekend assignments as events to Google 
        calendar.
        """
        for division in self.divisions.values():
            for block_num in range(len(division.assignments)):
                clinician = division.assignments[block_num]
                for j in range(BLOCK_SIZE, 0, -1):
                    week_start = datetime.strptime(
                        '2019/{0:02d}/1/08:00/'.format(
                            BLOCK_SIZE * (block_num + 1) - (j - 1)),
                        '%G/%V/%u/%H:%M/')
                    week_end = week_start + timedelta(hours=WEEK_HOURS)
                    summary = '{} - DIV:{} on call'.format(
                        clinician.name, division.name)
                    self._API.create_event(
                        week_start.isoformat(),
                        week_end.isoformat(),
                        [clinician.email],
                        summary
                    )

        for clinician in self.clinicians.values():
            for week_num in clinician.weekends_assigned:
                weekend_start = datetime.strptime(
                    '2019/{0:02d}/5/17:00/'.format(week_num),
                    '%G/%V/%u/%H:%M/')
                weekend_end = weekend_start + timedelta(hours=WEEKEND_HOURS)
                summary = '{} - on call'.format(clinician.name)
                self._API.create_event(
                    weekend_start.isoformat(),
                    weekend_end.isoformat(),
                    [clinician.email],
                    summary
                )


class API:
    """
    A helper class that wraps some of the API methods of Google calendar.
    """
    SCOPE = 'https://www.googleapis.com/auth/calendar'

    def __init__(self, secret_path, calendar_id, settings):
        self._store = file.Storage('credentials.json')
        self._creds = self._store.get()
        if not self._creds or self._creds.invalid:
            self._flow = client.flow_from_clientsecrets(
                secret_path, API.SCOPE)
            self._creds = tools.run_flow(self._flow, self._store)
        self._service = build(
            'calendar', 'v3', http=self._creds.authorize(Http()))

        self.calendar_id = calendar_id
        self.settings = settings
        self.time_zone = self.get_timezone()

    def get_timezone(self):
        """
        Returns the timezone of the calendar given by `calendar_id`.
        
        When possible, reads info from the settings file.
        """
        # pylint: disable=maybe-no-member
        tz = self.settings['time_zone']
        if tz:
            return tz
        else:
            result = self._service.calendars().get(
                calendarId=self.calendar_id).execute()
            self.settings['time_zone'] = result.get('timeZone')
            return self.settings['time_zone']

    def get_events(self, start, max_res=100):
        """
        Returns a list of at most `max_res` events whose start date is
        at the earliest `start`.
        """
        # pylint: disable=maybe-no-member
        result = self._service.events().list(
            calendarId=self.calendar_id,
            timeMin=start,
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
