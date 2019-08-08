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
delta_uncorrect = depart_conv - datetime.now() 
print (delta_uncorrect)
delta = delta_uncorrect - datetime(1900,1,1,0,0,0,0)
print (delta)
