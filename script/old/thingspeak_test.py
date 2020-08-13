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
    last_entry_D1 = jsonobj2["feeds"][0]["created_at"]
except:
    tempD1 = jsonobj2["feeds"][0]["field1"]
    humiD1 = jsonobj2["feeds"][0]["field2"]
    last_entry_D1 = jsonobj2["feeds"][0]["created_at"]

print (str(tempD1)+'°C  '+str(humiD1))
print (str(last_entry_D1))
last_entry_D1_dt = parser.parse(last_entry_D1)
print (last_entry_D1_dt)

ZERO = datetime.timedelta(0)

class UTC(datetime.tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()

delta = datetime.datetime.now(utc) - last_entry_D1_dt
print (delta)
sixminutes = datetime.timedelta(minutes=6)
if delta < sixminutes:
    print ('alles i.O!')
if delta > sixminutes:
    print ('offline')
