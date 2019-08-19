import json
import requests
import http.client, urllib.parse
data2 = requests.get(url="https://api.thingspeak.com/channels/843073/feeds.json?results=1")
jsonobj2 = json.loads(data2.content.decode('utf-8'))
try:
    tempD1 = round(float(jsonobj2["feeds"][0]["field1"]))
    humiD1 = round(float(jsonobj2["feeds"][0]["field2"]))
    last_entry_D1 = jsonobj2["channel"]["updated_at"]
except:
    tempD1 = jsonobj2["feeds"][0]["field1"]
    humiD1 = jsonobj2["feeds"][0]["field2"]
    
#calculate deltas
try:
    deltaT = round(float(tempPi1) - float(tempD1))
    deltaH = round(float(humiPi1) - float(humiD1))
except:
    deltaT = 'err'
    deltaH = 'err'
print (str(tempD1)+'°C  '+str(humiD1))
print (str(last_entry_D1))
