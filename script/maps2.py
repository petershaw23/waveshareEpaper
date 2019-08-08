import json, requests, pprint
import credentialsmaps
maps_key = credentialsmaps.maps_key
maps_key
url = "https://maps.googleapis.com/maps/api/directions/json?origin=Brooklyn&destination=Queens&mode=transit&key=" + maps_key
data = requests.get(url=url)
binary = data.content
output = json.loads(binary)

# test to see if the request was valid
print (output['status'])

# output all of the results
pprint.pprint(output)
