#only works with prior oauth via google api. need files "token.pickle" and/or (?) credentials.json in same dir! read https://developers.google.com/calendar/quickstart/python for info
from datetime import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time. 

if os.path.exists('token.pickle'):
     with open('token.pickle', 'rb') as token:
         creds = pickle.load(token)
if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    #IDs: 
    # Geburtstage: f89cl7qbv0ucgern33rhrtucno@group.calendar.google.com
    #Feiertage BW: k75hu0b8pa0t6j07h2f9v7i7553ftfoo@import.calendar.google.com
    #Feiertage D: de.german#holiday@group.v.calendar.google.com
    #Geli: v3bler8b7dm7h4uchn6mm5v01k@group.calendar.google.com
now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
#print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='f89cl7qbv0ucgern33rhrtucno@group.calendar.google.com', timeMin=now, timeMax=tomorrow, maxResults=10, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])
if not events:
    geb = ('kein bday!') #output, if no bday is found for the day
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    rawGeb = (start, event['summary'])
    print ('Geburtstage gcal.py: ' +str(rawGeb))
    geb = rawGeb[1] #<- this variable is called in uhr.py
