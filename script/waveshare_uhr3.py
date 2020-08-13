#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v3 by petershaw23 - shows time, date, current bday, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('------------------------')
#import datetime
from datetime import timedelta
from datetime import datetime
import json
import requests
import http.client, urllib.parse
import io
import sys
sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7 #lib fuer display
import epdconfig #config fuer display
from PIL import Image,ImageDraw,ImageFont
import subprocess, os
from dateutil import parser
import time

Datum = datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)


#manual calendar, to not be reliant on google api
fileName = open("/home/pi/script/waveshareEpaper/script/geburtstage.txt", 'r') 
today = datetime.now().strftime('%d.%m')
tomorrowRaw = datetime.now() + timedelta(days=1)
tomorrow = tomorrowRaw.strftime('%d.%m') 
in2daysRaw = datetime.now() + timedelta(days=2)
in2days = in2daysRaw.strftime('%d.%m') 
in3daysRaw = datetime.now() + timedelta(days=3)
in3days = in3daysRaw.strftime('%d.%m') 
in4daysRaw = datetime.now() + timedelta(days=4)
in4days = in4daysRaw.strftime('%d.%m') 
countdown = ""
geb = ""
count = 0

for line in fileName: 
    if today in line and count == 0: 
        line = line.split(' ') 
        geb = line[1]
        countdown = "heute: "
        print(str(countdown) + str(geb))
        count +=1
    if tomorrow in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "mrgn: "
        print(str(countdown) + str(geb))
        count +=1
    if in2days in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "t-2: "
        print(str(countdown) + str(geb))
        count +=1
    if in3days in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "t-3: "
        print(str(countdown) + str(geb))
        count +=1
    if in4days in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "t-4: "
        print(str(countdown) + str(geb))
        count +=1
    


f = open("/sys/class/thermal/thermal_zone0/temp", "r") #raspberry pi CPU temp
traw = f.readline ()
t = round(float(traw) / 1000)


# temperatur und humidity von thingspeak channel holen
# pi1 data
data1 = requests.get(url="https://api.thingspeak.com/channels/647418/feeds.json?results=1")
jsonobj1 = json.loads(data1.content.decode('utf-8'))
tempPi1 = round(float(jsonobj1["feeds"][0]["field3"]))
humiPi1 = round(float(jsonobj1["feeds"][0]["field5"]))

# d1 mini data
data2 = requests.get(url="https://api.thingspeak.com/channels/843073/feeds.json?results=1")
jsonobj2 = json.loads(data2.content.decode('utf-8'))
try:
    tempD1 = round(float(jsonobj2["feeds"][0]["field1"]))
    humiD1 = round(float(jsonobj2["feeds"][0]["field2"]))
    last_entry_D1 = jsonobj2["feeds"][0]["created_at"] #time of last entry
except: #if entry is Null
    tempD1 = jsonobj2["feeds"][0]["field1"] #displays the field entry (e.g. null)
    humiD1 = jsonobj2["feeds"][0]["field2"] #displays the field entry (e.g. null)
    last_entry_D1 = jsonobj2["feeds"][0]["created_at"] #same as in try

# time conversion of last entry, check if its older than 6 minutes (indicates f.ex. emtpy battery of D1 sensor)    
last_entry_D1_dt = parser.parse(last_entry_D1)   
ZERO = timedelta(0)
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
    print ('D1 status indicator: √')
    d1_status_indicator = str('√')
if delta > sixminutes:
    print ('D1 status indicator: X')
    d1_status_indicator = str('X')
 
#calculate deltaT and deltaH
try:
    deltaT = round(float(tempPi1) - float(tempD1))
    deltaH = round(float(humiPi1) - float(humiD1))
except:
    deltaT = 'err'
    deltaH = 'err'
print (str(t)+'°C   in: '+str(tempPi1)+'°C  '+str(humiPi1)+str('%    out: ')+str(tempD1)+'°C  '+str(humiD1)+str('%    Δt: ' )+str(deltaT)+str('°C   ΔH: ' )+str(deltaH))
    
# track ID via volumio REST api holen:

trackid = subprocess.Popen("curl 192.168.0.164/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputRAW, error) = trackid.communicate()
if trackid.returncode != 0: #if offline
   artist = ' '
   trackname = ' '
   #trackIDString = '        Volumio Offline' # placeholder for test 
   trackIDString = '- - - - - - - - - - - - - - - - - - - - -'
else:
   trackname = outputRAW.decode().split('\"')[9]
   artist = outputRAW.decode().split('\"')[13]
   trackIDString = (str(artist)+str(' - ')+str(trackname))
   #albumart = outputRAW.decode().split('\"')[21] #das waere sau cool

print (trackIDString)
######################################################################################################
#schriftarten definieren
fontXXL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 107) # font for time
fontXL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 32) # font for date
fontL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 28) # font for bday1
fontM = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 24) # font for volumio track ID
fontS = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 21) # font for bday2
fontXS = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 17) # font for temp, humi, cpu_temp
########################################################################################################
##############
#draw function
##############
def main():
        #Init driver
        epd = epd2in7.EPD()
        epd.init()
        # Image with screen size
        #255: clear the image with white
        image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        #Object image on which we will draw
        draw = ImageDraw.Draw(image)
        
        
        #draw.rectangle((0, 0, 264, 49), fill = 0) #rectangle behind bdays and date
        draw.rectangle((0, 48, 264, 71), fill = 0) #rectangle behind track ID
        draw.text((0, -7), str(Datum)+str(' ')+str(countdown)+str(geb), font = fontXL, fill = 0)              # Date + next bday
        #draw.text((75, -6), gebStringNext, font = fontL, fill = 0)     # bday1 old version, different size than date
        draw.line((5, 26, 259, 26), fill = 0)
        #### draw.text((0, 23), gebStringUeberNext, font = fontS, fill = 0) #bday2
        #draw.line((0, 48, 264, 48), fill = 0) # black line below bday 2
        #draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        #draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        draw.text((0, 45), trackIDString, font = fontM, fill = 1)       # volumio track ID
        #draw.line((0, 77, 264, 77), fill = 0)
        draw.text((-4, 53), Uhrzeit, font = fontXXL, fill = 0)           # time
        draw.line((0, 160, 264, 160), fill = 0)
        draw.text((120, 110), str(t),font = fontXS, fill = 0)             #cpu temp
        draw.text((121, 125), str(d1_status_indicator),font = fontXS, fill = 0)             #D1 Status Indicator (X or √)
        draw.text((0, 159), 'i:'+str(tempPi1)+'°|'+str(humiPi1)+str('%  o:')+str(tempD1)+'°|'+str(humiD1)+str('%  Δt:' )+str(deltaT)+str('°|ΔH:' )+str(deltaH)+str('%'), font = fontXS, fill = 0)       #temps
        

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()
 

if __name__ == '__main__':
    main()

