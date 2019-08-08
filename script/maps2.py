import json, requests, pprint

url = 'http://maps.googleapis.com/maps/api/directions/json?'

params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
)


data = requests.get(url=url, params=params)
binary = data.content
output = json.loads(binary)

# test to see if the request was valid
#print output['status']

# output all of the results
#pprint.pprint(output)

# step-by-step directions
for route in output['routes']:
        for leg in route['legs']:
            for step in leg['steps']:
                print step['html_instructions']
