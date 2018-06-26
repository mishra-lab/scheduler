import json
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools
from ortools.linear_solver import pywraplp

NUM_WEEKS = 52
# mon 8am + 105 hours = fri 5pm
# 105 = 4 * 24hr + (17hr - 8hr)
WEEK_HOURS = 24 * 4 + (17 - 8)


class Clinician:
    def __init__(self, name, min_, max_, email, weeks_off):
        self.name = name
        self.min = min_
        self.max = max_
        self.email = email
        self.weeks_off = weeks_off
        self.weeks_assigned = []

        self._vars = [[]] * NUM_WEEKS

    def get_vars(self):
        return self._vars

    def get_var(self, week):
        return self._vars[week]

    def set_var(self, week, val):
        self._vars[week] = val

    def get_value(self, week):
        return self._vars[week].solution_value()


class Scheduler:
    def __init__(self, settings):
        secret_path = '../config/client_secret.json'
        calendar_id = 'primary'

        secret_path = settings.get_path_from_key('secret_path')
        calendar_id = settings['calendar_id']
        self.clinic_conf = settings.get_path_from_key('clinician_config_path')

        self._API = API(secret_path, calendar_id, settings)
        self.clinicians = {}
        # self.network = FlowNetwork()
        self.lpSolver = pywraplp.Solver(
            'scheduler', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    def read_clinic_conf(self):
        with open(self.clinic_conf, 'r') as f:
            data = json.load(f)
            for clinician in data:
                self.clinicians[clinician] = \
                    Clinician(
                        name=clinician,
                        min_=data[clinician]['min'],
                        max_=data[clinician]['max'],
                        email=data[clinician]['email'] if 'email' in data[clinician] else '',
                        weeks_off=[]
                )

    def populate_weeks_off_from_file(self, data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
            for clinician in data:
                self.clinicians[clinician].weeks_off = data[clinician]['weeks_off']

    def populate_weeks_off(self):
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

            # figure out if this time-off request covers a week
            # if not, we can safely ignore it
            covers_week = False
            curr = start
            while curr < end:
                if curr.isoweekday() in range(1, 6):
                    covers_week = True
                    break
                curr += timedelta(days=1)

            if covers_week:
                if creator in self.clinicians:
                    week_range = list(
                        range(start.isocalendar()[1], end.isocalendar()[1] + 1))
                    for week in week_range:
                        self.clinicians[creator].weeks_off.append(week - 1)

    def build_lp(self):
        helpers = {}

        for clinician in self.clinicians.values():
            for j in range(NUM_WEEKS):
                clinician.set_var(j, self.lpSolver.IntVar(
                    0, 1, '{},{}'.format(clinician.name, j)
                ))

        # no holes + no overlap
        for j in range(NUM_WEEKS):
            vars_ = []
            for clinician in self.clinicians.values():
                vars_.append(clinician.get_var(j))
            self.lpSolver.Add(self.lpSolver.Sum(vars_) == 1)

        # mins/maxes
        for clinician in self.clinicians.values():
            self.lpSolver.Add(self.lpSolver.Sum(
                clinician.get_vars()) <= clinician.max)
            self.lpSolver.Add(-self.lpSolver.Sum(clinician.get_vars())
                              <= -clinician.min)

        # at most 2 consective weeks of work
        for clinician in self.clinicians.values():
            for j in range(NUM_WEEKS - 2):
                self.lpSolver.Add(clinician.get_var(
                    j) + clinician.get_var(j + 1) + clinician.get_var(j + 2) <= 2)

        # initialize helper vars used to maximize product of vars
        for clinician in self.clinicians.values():
            helpers[clinician.name] = []
            for j in range(NUM_WEEKS - 1):
                helpers[clinician.name].append(self.lpSolver.IntVar(
                    0, 1, '{0},{1}*{0},{2}'.format(clinician.name, j, j+1)))
                self.lpSolver.Add(
                    helpers[clinician.name][j] <= clinician.get_var(j))
                self.lpSolver.Add(
                    helpers[clinician.name][j] <= clinician.get_var(j))

        # build objective function
        block_count = self.lpSolver.Sum(
            (helpers[clin.name][j]) for clin in self.clinicians.values() for j in range(NUM_WEEKS - 1)
        )
        appeasement_count = self.lpSolver.Sum(
            (0 if j in clin.weeks_off else clin.get_var(j)) for clin in self.clinicians.values() for j in range(NUM_WEEKS))
        self.lpSolver.Maximize(
            0.5 * appeasement_count +
            0.5 * block_count)

    def solve_lp(self):
        self.lpSolver.Solve()

    def assign_weeks(self):
        for clin in self.clinicians.values():
            for j in range(NUM_WEEKS):
                if clin.get_var(j).solution_value() == 1.0:
                    clin.weeks_assigned.append(j)

        # create events for weeks assigned
        for clin in self.clinicians.values():
            for week_num in clin.weeks_assigned:
                week_start = datetime.strptime(
                    '2019/{0:02d}/1/08:00/'.format(week_num + 1),
                    '%G/%V/%u/%H:%M/')
                week_end = week_start + timedelta(hours=WEEK_HOURS)
                summary = '{} - on call'.format(clin.name)
                self._API.create_event(
                    week_start.isoformat(),
                    week_end.isoformat(),
                    [clin.email],
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
