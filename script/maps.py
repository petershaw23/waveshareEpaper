#!/usr/bin/python3
import googlemaps
import json
from datetime import datetime
import credentialsmaps
maps_key = credentialsmaps.maps_key
gmaps = googlemaps.Client(key=maps_key)

# Request directions via public transit
now = datetime.now()
data = gmaps.directions("Sydney Town Hall", "Parramatta, NSW", mode="transit", departure_time=now)
my_json_string = json.dumps(data)
y = json.loads(my_json_string)

# the result is a Python dictionary:
print(y[3]) 
