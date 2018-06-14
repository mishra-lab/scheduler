from netflow import FlowVertex, FlowArc, FlowNetwork
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, timedelta
import json

NUM_WEEKS = 52


class Scheduler:
    def __init__(self, settings_file=None):
        secret_path = '../client_secret.json'
        calendar_id = 'primary'

        if settings_file:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                secret_path = settings['secret_path']
                calendar_id = settings['calendar_id']
                self.clinic_conf = settings['clinician_config']

        self._API = API(secret_path, calendar_id)
        self.clinicians = {}
        self.network = FlowNetwork()

    def read_clinic_conf(self):
        with open(self.clinic_conf, 'r') as f:
            self.clinicians = json.load(f)

    def populate_weeks_off_from_file(self, data_file):
        clinicians = {}
        with open(data_file, 'r') as f:
            clinicians = json.load(f)

        for clinician in clinicians:
            if clinician in self.clinicians:
                self.clinicians[clinician]['weeks_off'] = clinicians[clinician]['weeks_off']

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
                        if 'weeks_off' not in self.clinicians[creator]:
                            self.clinicians[creator]['weeks_off'] = []
                        self.clinicians[creator]['weeks_off'].append(str(week))

    def build_net(self):
        self.network.add_vertex(FlowVertex('source', NUM_WEEKS))
        self.network.add_vertex(FlowVertex('sink', -NUM_WEEKS))
        # add circulation arc
        self.network.add_arc(FlowArc(
            FlowVertex.get_vertex('sink'),
            FlowVertex.get_vertex('source'),
            min_cap=0,
            max_cap=NUM_WEEKS*2,
            cost=0,
            fixed_cost=True)
        )

        # add vertices for each week + arcs to sink
        for i in range(0, NUM_WEEKS):
            self.network.add_vertex(FlowVertex(str(i+1), 0))
            self.network.add_arc(
                FlowArc(
                    FlowVertex.get_vertex(str(i+1)),
                    FlowVertex.get_vertex('sink'),
                    min_cap=1,
                    max_cap=1,
                    cost=0,
                    fixed_cost=True)
            )

        # add vertices for each clinican, an arc from source to clinician
        # and an arc from clinician to each week
        for name in self.clinicians:
            self.network.add_vertex(FlowVertex(name, 0))
            clinician = self.clinicians[name]
            self.network.add_arc(
                FlowArc(
                    FlowVertex.get_vertex('source'),
                    FlowVertex.get_vertex(name),
                    min_cap=clinician['min'],
                    max_cap=clinician['max'],
                    cost=0,
                    fixed_cost=True)
            )
            for i in range(0, NUM_WEEKS):
                self.network.add_arc(
                    FlowArc(
                        FlowVertex.get_vertex(name),
                        FlowVertex.get_vertex(str(i+1)),
                        min_cap=0,
                        max_cap=1,
                        cost=1000 if i+1 in clinician['weeks_off'] else 1,
                        fixed_cost=True if i+1 in clinician['weeks_off'] else False)
                )

    def assign_weeks(self):
        for clinician in self.clinicians:
            if 'weeks_assigned' not in self.clinicians[clinician]:
                self.clinicians[clinician]['weeks_assigned'] = []
            clin_vert = FlowVertex.get_vertex(clinician)
            for arc in clin_vert.out_arcs:
                if arc.flow > 0:
                    # make sure we didn't assign a week off
                    assert int(
                        arc.dest_vert.name) not in self.clinicians[clinician]['weeks_off']
                    self.clinicians[clinician]['weeks_assigned'].append(
                        int(arc.dest_vert.name))


class API:
    SCOPE = 'https://www.googleapis.com/auth/calendar'

    def __init__(self, secret_path, calendar_id):
        self._store = file.Storage('credentials.json')
        self._creds = self._store.get()
        if not self._creds or self._creds.invalid:
            self._flow = client.flow_from_clientsecrets(
                secret_path, API.SCOPE)
            self._creds = tools.run_flow(self._flow, self._store)
        self._service = build(
            'calendar', 'v3', http=self._creds.authorize(Http()))

        self.calendar_id = calendar_id

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
        event = {
            'summary': summary,
            'start': {
                'date': start
            },
            'end': {
                'date': end
            },
            'attendees': [
                {'email': _} for _ in attendees
            ]
        }

        self._service.events().insert(
            calendarId=self.calendar_id,
            body=event
        ).execute()