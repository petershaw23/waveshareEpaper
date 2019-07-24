#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v2 by petershaw23 - shows time, date, google calendar current bday, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('-----------------------------')
from datetime import datetime
Datum = datetime.now().strftime('%d.%m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)
# google API get bdays
try:
    import gcallite #imports gcallite.py from same directory. if this script is executed via cronjob, check env. settings! or use attached bash file "exec.sh" to oauth instead
    geb = gcallite.geb #call variable from imported file. should be a name or 'kein geb'
except: #falls fehler
    geb = 'error'
print ('Output in uhr.py: '+str(geb))
###
import io
f = open("/sys/class/thermal/thermal_zone0/temp", "r") #raspberry pi CPU temp
traw = f.readline ()
t = round(float(traw) / 1000)
###
import sys
sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7 #lib fuer display
import epdconfig #config fuer display
from PIL import Image,ImageDraw,ImageFont
###
# temperatur und humidity von thingspeak channel holen
try:
    import thingspeak
    ch = thingspeak.Channel(647418)
    outRAW = ch.get({'results':1})
    outSplit = outRAW.split('\"')
    outTemp = outSplit[-18]
    outHumi = outSplit[-14]
except: #falls offline
    outTemp = '??'
    outHumi = '??'
print ('thingspeak: temp '+str(outTemp)+'  humidity: '+str(outHumi))

#schriftarten definieren
font24 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 102) #font for time
font18 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 33) #font for date, bday
font14 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 21) #font for volumio track ID
font8 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 16) #font for temp, humi, cpu_temp
# track ID via volumio REST api holen:
import subprocess, os
trackid = subprocess.Popen("curl 192.168.0.241/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputRAW, error) = trackid.communicate()
if trackid.returncode != 0: #if offline
   artist = '- multiroom audio offline'
   trackname = ''
else:
   trackname = outputRAW.decode().split('\"')[9]
   artist = outputRAW.decode().split('\"')[13]
   #albumart = outputRAW.decode().split('\"')[21] #das waere sau cool

print (str(artist)+str(' - ')+str(trackname))


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
        draw.text((5, -7), Datum, font = font18, fill = 0) #Date
        draw.text((106, -7), geb, font = font18, fill = 0) #bday
        draw.text((0, 160), str(t) +' °C', font = font8, fill = 0) #CPU temp
        draw.text((158, 160), str(outTemp) +'°C    ' +str(outHumi) +str('%'), font = font8, fill = 0) #Temp+Humidity
        draw.text((5, 39), str(artist)+str(' - ')+str(trackname), font = font14, fill = 0) #volumio track ID
        draw.text((5, 55), Uhrzeit, font = font24, fill = 0) #time

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()

if __name__ == '__main__':
    main()
