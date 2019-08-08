#!/usr/bin/python3
import googlemaps
import json
from datetime import datetime
import credentialsmaps
maps_key = credentialsmaps.maps_key
gmaps = googlemaps.Client(key=maps_key)

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)
                                     
jsonliste=json.loads(str(directions_result))
print(jsonliste['departure_time'])
