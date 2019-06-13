import os
import sys
import argparse

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client import file as oauth_file
from oauth2client import tools


class ApiHelper:
    """
    A helper class that wraps some of the API methods of Google calendar.
    """
    SCOPE = 'https://www.googleapis.com/auth/calendar'

    def __init__(self, calendar_id):
        # retrieve credentials / create new
        store = oauth_file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                self.get_client_secret(), ApiHelper.SCOPE)

            # hack: force gapi library to use port 443
            flags = tools.argparser.parse_args()
            flags.auth_host_port = [443]

            creds = tools.run_flow(flow, store, flags=flags)

        # discover calendar API
        self._service = build(
            'calendar', 'v3', http=creds.authorize(Http()))
        self.calendar_id = calendar_id
        self.time_zone = self.get_timezone()

    def get_client_secret(self):
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

    def get_events(self, start, end, search_str='', max_res=1000):
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

        events = result.get('items', [])
        return list(filter(lambda x, s=search_str: s in x['summary'], events))

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

    def delete_event(self, event_id):
        # pylint: disable=maybe-no-member
        self._service.events().delete(
            calendarId=self.calendar_id,
            eventId=event_id
        ).execute()

    def delete_events(self, start, end, search_str=''):
        events = self.get_events(start, end, search_str)

        for event in events:
            id_ = event['id']
            self.delete_event(id_)
