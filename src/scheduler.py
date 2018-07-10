import json
import math
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from ortools.linear_solver import pywraplp

NUM_BLOCKS = 26
# mon 8am + 105 hours = fri 5pm
# 105 = 4 * 24hr + (17hr - 8hr)
WEEK_HOURS = 24 * 4 + (17 - 8)

BLOCK_SIZE = 2


class Variable:
    def __init__(self):
        raise NotImplementedError()

    def get_value(self):
        raise NotImplementedError()


class WeekendVariable(Variable):
    def __init__(self, clinician, week_num, lpSolver):
        self.clinician = clinician
        self.week_num = week_num

        self._var = lpSolver.IntVar(
            0, 1, '{},weekend:{}'.format(
                self.clinician.name, self.week_num
            )
        )

    def get_var(self):
        return self._var

    def get_value(self):
        return self._var.solution_value()


class BlockVariable(Variable):
    def __init__(self, clinician, block_num, division, lpSolver):
        self.clinician = clinician
        self.block_num = block_num
        self.division = division

        # register variable in LP solver
        self._var = lpSolver.IntVar(
            0, 1, '{},div:{},block:{}'.format(
                self.clinician.name, self.division, self.block_num))

    def get_var(self):
        return self._var

    def get_value(self):
        return self._var.solution_value()


class Division:
    def __init__(self, name):
        self.name = name
        self.clinicians = []
        self.bound_dict = dict()

        self.assignments = []

    def add_clinician(self, clinician, min_, max_):
        if clinician not in self.clinicians:
            self.clinicians.append(clinician)
            self.bound_dict[clinician.name] = (min_, max_)

    def remove_clinician(self, clinician, min_, max_):
        if clinician in self.clinicians:
            del self.bound_dict[clinician.name]
            self.clinicians.remove(clinician)

    def get_vars(self):
        """
        Returns all BlockVariables corresponding to this division, across all
        clinicians.
        """
        block_vars = [
            _ for clinician in self.clinicians for _ in clinician.get_block_vars()]
        return list(filter(lambda x: x.division == self.name, block_vars))

    def get_vars_by_block_num(self, block_num):
        return list(filter(lambda x: x.block_num == block_num, self.get_vars()))

    def get_vars_by_name(self, name):
        return list(filter(lambda x: x.clinician.name == name, self.get_vars()))


class Clinician:
    def __init__(self, name, email, blocks_off=[], weekends_off=[]):
        self.name = name
        self.email = email
        self.blocks_off = blocks_off
        self.blocks_assigned = []
        self.weekends_off = weekends_off
        self.weekends_assigned = []

        self._vars = []

    def add_var(self, var):
        if var not in self._vars:
            self._vars.append(var)

    def remove_var(self, var):
        if var in self._vars:
            self._vars.remove(var)

    def get_vars(self, predicate=None):
        return list(filter(predicate, self._vars))

    def get_block_vars(self, predicate=None):
        return list(filter(predicate, self.get_vars(lambda x: type(x) is BlockVariable)))

    def get_weekend_vars(self, predicate=None):
        return list(filter(predicate, self.get_vars(lambda x: type(x) is WeekendVariable)))


class Scheduler:
    def __init__(self, settings):
        secret_path = '../config/client_secret.json'
        calendar_id = 'primary'

        secret_path = settings.get_path_from_key('secret_path')
        calendar_id = settings['calendar_id']
        self.config_file = settings.get_path_from_key('clinician_config_path')

        self._API = API(secret_path, calendar_id, settings)
        self.clinicians = {}
        self.divisions = {}
        self.lpSolver = pywraplp.Solver(
            'scheduler', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    def read_config(self):
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

    def read_calendar(self):
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

    def build_lp(self):
        # create clinician BlockVariables
        for div in self.divisions.values():
            for clinician in div.clinicians:
                for block_num in range(1, NUM_BLOCKS + 1):
                    clinician.add_var(
                        BlockVariable(clinician, block_num,
                                      div.name, self.lpSolver)
                    )
        # create clinician WeekendVariables
        # for clinician in self.clinicians.values():
        #     for week_num in range(NUM_BLOCKS * BLOCK_SIZE):
        #         clinician.add_var(
        #             WeekendVariable(clinician, week_num, self.lpSolver)
        #         )

        # no holes + no overlap over all divisions (BLOCKS)
        for div in self.divisions.values():
            for block_num in range(1, NUM_BLOCKS + 1):
                self.lpSolver.Add(
                    self.lpSolver.Sum(
                        [_.get_var()
                         for _ in div.get_vars_by_block_num(block_num)]
                    ) == 1
                )

        # no holes + no overlap (WEEKENDS)
        # for clinician in self.clinicians.values():
        #     for week_num in range(NUM_BLOCKS * BLOCK_SIZE):
        #         vars_ = clinician.get_weekend_vars(lambda x, week_num=week_num: x.week_num == week_num)
        #         self.lpSolver.Add(self.lpSolver.Sum([_.get_var() for _ in vars_]) == 1)

        # mins/maxes per division
        for div in self.divisions.values():
            for clinician in div.clinicians:
                (min_, max_) = div.bound_dict[clinician.name]
                sum_ = self.lpSolver.Sum(
                    [_.get_var() for _ in div.get_vars_by_name(clinician.name)])
                self.lpSolver.Add(sum_ <= max_)
                self.lpSolver.Add(-sum_ <= -min_)

        for clinician in self.clinicians.values():
            for block_num in range(1, NUM_BLOCKS):
                # if a clinician works a given blocks, they should not work any
                # adjacent block (even in a different division)
                sum_ = self.lpSolver.Sum(
                    [_.get_var() for _ in clinician.get_block_vars(
                        lambda x, block_num=block_num: x.block_num in (block_num, block_num + 1))]
                )
                self.lpSolver.Add(sum_ <= 1)

            # at most 1 consecutive weekend of work
            # for week_num in range((NUM_BLOCKS * BLOCK_SIZE) - 1):
            #     sum_ = self.lpSolver.Sum(
            #         [_.get_var() for _ in clinician.get_weekend_vars(lambda x, week_num=week_num: x.week_num in (week_num, week_num + 1))]
            #     )
            #     self.lpSolver.Add(sum_ <= 1)

        # objective functions
        ba_variables = []
        for clinician in self.clinicians.values():
            ba_variables.extend(
                [_.get_var() for _ in clinician.get_block_vars(
                    lambda x, clinician=clinician: x.block_num not in clinician.blocks_off)]
            )

            ba_variables.extend(
                [-_.get_var() for _ in clinician.get_block_vars(lambda x,
                                                                clinician=clinician: x.block_num in clinician.blocks_off)]
            )
        block_appeasement_count = self.lpSolver.Sum(ba_variables)

        # wa_variables = []
        # for clinician in self.clinicians.values():
        #     wa_variables.extend(
        #         [_.get_var() for _ in clinician.get_weekend_vars(lambda x, clinician=clinician: x.week_num not in clinician.weekends_off)]
        #     )

        #     wa_variables.extend(
        #         [-_.get_var() for _ in clinician.get_weekend_vars(lambda x, clinician=clinician: x.week_num in clinician.weekends_off)]
        #     )
        # weekend_appeasement_count = self.lpSolver.Sum(wa_variables)

        self.lpSolver.Maximize(
            block_appeasement_count
            # + weekend_appeasement_count
        )

    def solve_lp(self):
        ret = self.lpSolver.Solve() == self.lpSolver.OPTIMAL
        print('objective value = {}'.format(self.lpSolver.Objective().Value()))
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
        for div in self.divisions.values():
            for block_num in range(1, NUM_BLOCKS + 1):
                assignments = list(filter(lambda x: x.get_value(
                ) == 1.0, div.get_vars_by_block_num(block_num)))
                div.assignments.extend(
                    [_.clinician for _ in assignments]
                )

        for clinician in self.clinicians.values():
            clinician.weekends_assigned = clinician.get_weekend_vars(
                lambda x: x.get_value() == 1.0)

    def publish_schedule(self):
        for division in self.divisions.values():
            for block_num in range(len(division.assignments)):
                clinician = division.assignments[block_num]
                for j in range(BLOCK_SIZE, 0, -1):
                    week_start = datetime.strptime(
                        '2019/{0:02d}/1/08:00/'.format(
                            BLOCK_SIZE * (block_num + 1) - (j - 1)),
                        '%G/%V/%u/%H:%M/')
                    week_end = week_start + timedelta(hours=WEEK_HOURS)
                    summary = '{} - DIV:{} on call'.format(clinician.name, division.name)
                    self._API.create_event(
                        week_start.isoformat(),
                        week_end.isoformat(),
                        [clinician.email],
                        summary
                    )


class API:
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
        Returns the timezone of the calendar given by calendar_id.
        
        When possible, reads info from settings file.
        """
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
        Returns a list of at most max_res events beginning >= start.
        """
        result = self._service.events().list(
            calendarId=self.calendar_id,
            timeMin=start,
            maxResults=max_res,
            singleEvents=True,
            orderBy='startTime').execute()

        return result.get('items', [])

    def create_event(self, start, end, attendees, summary):
        """
        Creates a new event from start to end with the given attendees
        list and summary
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

        self._service.events().insert(
            calendarId=self.calendar_id,
            body=event
        ).execute()
