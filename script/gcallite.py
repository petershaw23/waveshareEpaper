#only works with prior oauth via google api. need files "token.pickle" and/or (?) credentials.json in same dir! read https://developers.google.com/calendar/quickstart/python for info
from datetime import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time. 

if os.path.exists('token.pickle'):
     with open('token.pickle', 'rb') as token:
         creds = pickle.load(token)

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
    geb = ('kein geb')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    rawGeb = (start, event['summary'])
    print ('Geburtstage gcal.py: ' +str(rawGeb))
    geb = rawGeb[1]
