import json
import math
from datetime import datetime, timedelta

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client, file, tools

from netflow import FlowArc, FlowNetwork, FlowVertex

NUM_BLOCKS = 3
# mon 8am + 105 hours = fri 5pm
# 105 = 4 * 24hr + (17hr - 8hr)
WEEK_HOURS = 24 * 4 + (17 - 8)

BLOCK_SIZE = 2


class Clinician:
    def __init__(self, name, min_, max_, email, blocks_off):
        self.name = name
        self.min = min_
        self.max = max_
        self.email = email
        self.blocks_off = blocks_off
        self.blocks_assigned = []

        self._vert = None

    def get_vert(self):
        return self._vert

    def set_vert(self, vert):
        self._vert = vert


class Scheduler:
    def __init__(self, settings):
        secret_path = '../config/client_secret.json'
        calendar_id = 'primary'

        secret_path = settings.get_path_from_key('secret_path')
        calendar_id = settings['calendar_id']
        self.clinic_conf = settings.get_path_from_key('clinician_config_path')

        self._API = API(secret_path, calendar_id, settings)
        self.clinicians = {}
        self.network = FlowNetwork()

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
                        blocks_off=[]
                )

    def populate_blocks_off_from_file(self, data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
            for clinician in data:
                self.clinicians[clinician].blocks_off = data[clinician]['blocks_off']

    def populate_blocks_off(self):
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
                    week_range = range(start.isocalendar()[
                                       1], end.isocalendar()[1] + 1, 2)
                    for week in week_range:
                        self.clinicians[creator].blocks_off.append(
                            math.ceil(week / BLOCK_SIZE)
                        )

    def build_net(self):
        self.network.add_vertex(FlowVertex('source', NUM_BLOCKS))
        self.network.add_vertex(FlowVertex('sink', -NUM_BLOCKS))
        # add circulation arc
        self.network.add_arc(FlowArc(
            FlowVertex.get_vertex('sink'),
            FlowVertex.get_vertex('source'),
            min_cap=0,
            max_cap=NUM_BLOCKS*2,
            cost=0,
            fixed_cost=True)
        )

        # add vertices for each block + arcs to sink
        for i in range(NUM_BLOCKS):
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
        # and an arc from clinician to each block
        for clin in self.clinicians.values():
            vert = FlowVertex(clin.name, 0)
            self.network.add_vertex(vert)
            clin.set_vert(vert)
            self.network.add_arc(
                FlowArc(
                    FlowVertex.get_vertex('source'),
                    FlowVertex.get_vertex(clin.name),
                    min_cap=clin.min,
                    max_cap=clin.max,
                    cost=0,
                    fixed_cost=True)
            )
            for i in range(0, NUM_BLOCKS):
                self.network.add_arc(
                    FlowArc(
                        FlowVertex.get_vertex(clin.name),
                        FlowVertex.get_vertex(str(i+1)),
                        min_cap=0,
                        max_cap=1,
                        cost=1000 if i+1 in clin.blocks_off else 1,
                        fixed_cost=True if i+1 in clin.blocks_off else False)
                )

    def assign_weeks(self):
        for clin in self.clinicians.values():
            vert = clin.get_vert()
            for arc in vert.out_arcs:
                if arc.flow > 0:
                    clin.blocks_assigned.append(int(arc.dest_vert.name))

        # create events for weeks assigned
        for clin in self.clinicians.values():
            for block_num in clin.blocks_assigned:
                for j in range(BLOCK_SIZE, 0, -1):
                    week_start = datetime.strptime(
                        '2019/{0:02d}/1/08:00/'.format(
                            BLOCK_SIZE * block_num - (j - 1)),
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
