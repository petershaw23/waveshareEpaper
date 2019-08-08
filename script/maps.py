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
print (data[0:3])
