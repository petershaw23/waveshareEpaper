#!/usr/bin/python3
import json
import requests
from datetime import datetime
from datetime import timedelta
import credentialsmaps # imports local file credentialmaps.py with google maps api key

maps_key = credentialsmaps.maps_key
url = "https://maps.googleapis.com/maps/api/directions/json?origin=Hauptbahnhof+Mannheim&destination=Hauptbahnhof+Heidelberg&language=de&mode=transit&key=" + maps_key
data = requests.get(url=url)
jsonobj = json.loads(data.content)
#print (jsonobj)

depart = (jsonobj["routes"][0]["legs"][0]["arrival_time"]["text"])
print (str('naechster zug: ')+str(depart))

depart_conv = datetime.strptime(depart, '%H:%M')
depart_minute = (depart_conv.minute)
print (depart_minute)
now = datetime.now() 
now_minute = now.minute
print (now_minute)
delta_minute = depart_minute - now_minute
print (delta_minute)
if delta_minute < 15 > 12:
    print ('das wird eng!')
elif delta_minute == 12:
    print ('jetzt losrennen!')
elif delta_minute < 12:
    print ('den kriegst du nicht mehr!')
#delta_uncorrect = depart_conv - datetime.now() 
#print (delta_uncorrect)


