import json
import requests
import credentialsmaps # imports local file credentialmaps.py with google maps api key
maps_key = credentialsmaps.maps_key
url = "https://maps.googleapis.com/maps/api/directions/json?origin=Hauptbahnhof+Mannheim&destination=Hauptbahnhof+Heidelberg&language=de&mode=transit&key=" + maps_key
data = requests.get(url=url)
binary = data.content
output = json.loads(binary)

# test to see if the request was valid

print (output)
print (output['status'])
print (output['routes'])

