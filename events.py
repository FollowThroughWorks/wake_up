import google_oauth2 # oauth
from apiclient.discovery import build

import datetime
import dateutil.parser as parser # formatting datetimes
from httplib2 import Http

GOOGLE_CREDENTIALS = google_oauth2.get_credentials()

# Google calendar events
class google_calendar:
    def __init__(self):
        print("Connecting to calendar...")
        self.service = build('calendar', 'v3', http=GOOGLE_CREDENTIALS.authorize(Http()))

    def events(self,span):
        print("Retrieving calendar info...")
        calendars = ['primary']
        today = parser.parse(str(datetime.date.today())).isoformat() + 'Z'
        tomorrow = parser.parse(str(datetime.date.today() + datetime.timedelta(days=1))).isoformat() + 'Z'
        five_days = parser.parse(str(datetime.date.today() + datetime.timedelta(days=5))).isoformat() + 'Z'

        if span == 'day': event_span = tomorrow
        else: event_span = five_days
        
        event_list = []
        for calendar in calendars:
            #self.event_list += self.service.events().list(calendarId = calendar, timeMin = today).execute().get('items', [])
            event_list += [event['summary'] for event in self.service.events().list(calendarId = calendar, timeMin = today, timeMax = event_span).execute().get('items', [])]

        if not event_list: event_list = ["You have no events."]
        return event_list
