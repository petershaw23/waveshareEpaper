import json
import requests
import http.client, urllib.parse
import datetime
from dateutil import parser
data2 = requests.get(url="https://api.thingspeak.com/channels/843073/feeds.json?results=1")
jsonobj2 = json.loads(data2.content.decode('utf-8'))
try:
    tempD1 = round(float(jsonobj2["feeds"][0]["field1"]))
    humiD1 = round(float(jsonobj2["feeds"][0]["field2"]))
    last_entry_D1 = jsonobj2["channel"]["updated_at"]
except:
    tempD1 = jsonobj2["feeds"][0]["field1"]
    humiD1 = jsonobj2["feeds"][0]["field2"]
    last_entry_D1 = jsonobj2["channel"]["updated_at"]

print (str(tempD1)+'°C  '+str(humiD1))
print (str(last_entry_D1))
last_entry_D1_dt = parser.parse(last_entry_D1)
delta = last_entry_D1_dt - datetime.datetime.now(timezone.utc)
print (delta)
