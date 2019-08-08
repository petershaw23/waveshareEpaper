import json
import requests
import credentialsmaps # imports local file credentialmaps.py with google maps api key
maps_key = credentialsmaps.maps_key
url = "https://maps.googleapis.com/maps/api/directions/json?origin=Hauptbahnhof+Mannheim&destination=Hauptbahnhof+Heidelberg&language=de&mode=transit&key=" + maps_key
data = requests.get(url=url)
jsonobj = json.loads(data.content)
#print (jsonobj)

print (jsonobj["routes"][0]["legs"][0]["arrival_time"][0]["text"])
