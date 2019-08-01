#only works with prior oauth via google api. need files "token.pickle" and/or (?) credentials.json in same dir! read https://developers.google.com/calendar/quickstart/python for info
from datetime import datetime
from datetime import timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from dateutil.parser import parse
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
    # my IDs, pls use your own :): 
    # Geburtstage: f89cl7qbv0ucgern33rhrtucno@group.calendar.google.com
    #Feiertage BW: k75hu0b8pa0t6j07h2f9v7i7553ftfoo@import.calendar.google.com
    #Feiertage D: de.german#holiday@group.v.calendar.google.com
    #and: v3bler8b7dm7h4uchn6mm5v01k@group.calendar.google.com
now = datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
today = (datetime.now() + timedelta(hours=1)).isoformat() + 'Z' # hint: 11 pm will display tomorrows birthday
tomorrow = (datetime.now() + timedelta(hours=24)).isoformat() + 'Z'
next_week = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'

# google calendar api get bdays in list
#geb = str(' ') 
list = [] #create emtpy list to put bdays in
events_result_next_geb = service.events().list(calendarId='f89cl7qbv0ucgern33rhrtucno@group.calendar.google.com', timeMin=now, timeMax=next_week, maxResults=10, singleEvents=True, orderBy='startTime').execute()
events_next_geb = events_result_next_geb.get('items', [])
if not events_next_geb:
    #geb_next = str(' ') #output, if no bdays are found
    #delta = str(' ')
    #geb = str(' ')
    #do nothing. list stays empty
    list = []
for event_next_geb in events_next_geb:
    start = event_next_geb['start'].get('dateTime', event_next_geb['start'].get('date'))
    rawGeb_next = (start, event_next_geb['summary'])
    #print (str(rawGeb_next))
    #start_conv = datetime.strptime(start, '%Y-%m-%d')
    #deltaRaw = start_conv - datetime.now()
    #delta = (deltaRaw.days + 1)
    #if delta > 0: #if the bday is not today
       #print ('nicht heute!')
    list.append(rawGeb_next)
    #else:
       #print ('heute!') #if the bday is today
      # geb = rawGeb_next[1]
       #print (geb)

#print ('____')
#print (list)
#print (geb)
