#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v2 by psw - zeigt  Uhrzeit, Datum, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('-----------------------------')
import io
f = open("/sys/class/thermal/thermal_zone0/temp", "r") #raspberry pi CPU temp
traw = f.readline ()
t = round(float(traw) / 1000)
import sys
sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7 #lib fuer display
import epdconfig #config fuer display
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
Datum = datetime.now().strftime('%d.%m.')
Uhrzeit = datetime.now().strftime('%H:%M')

import thingspeak #temperatur und humidity von thingspeak channel holen
try:
    import gcallite
    geb = gcallite.heuteGeb[1]
    print('Output: '+str(geb))
except:
    print ('failed to import gcallite')
try:
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
font24 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 102)
font18 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 34)
font14 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 23)
font8 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 14)
# track ID via volumio REST api holen:
import subprocess, os
trackid = subprocess.Popen("curl 192.168.0.241/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputRAW, error) = trackid.communicate()
if trackid.returncode != 0:
  # print('Schlafzimmer aus?')
   artist = 'off'
   trackname = 'line'
   print (str(artist)+str(' - ')+str(trackname))
else:
   #print(outputRAW)
   trackname = outputRAW.decode().split('\"')[9]
   artist = outputRAW.decode().split('\"')[13]
   #albumart = outputRAW.decode().split('\"')[21]
   print (str(artist)+str(' - ')+str(trackname))
   #print (albumart)


def main():
        #Init driver
        epd = epd2in7.EPD()
        print(Datum, Uhrzeit)
        #print("init")
        epd.init()

        # Image with screen size
        #255: clear the image with white
        image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        #Object image on which we will draw
        draw = ImageDraw.Draw(image)

        #draw a rectangle in the center of the screen
        #draw.rectangle((epd2in7.EPD_WIDTH/2-10, epd2in7.EPD_HEIGHT/2-10, epd2in7.EPD_WIDTH/2+10, epd2in7.EPD_HEIGHT/2+10), fill = 0)

        draw.text((45, -7), Datum, font = font18, fill = 0) #Datm
        draw.text((130, -7), geb, font = font18, fill = 0)
        draw.text((0, 162), str(t) +' °C', font = font8, fill = 0) #CPU temp
        draw.text((165, 162), str(outTemp) +'°C    ' +str(outHumi) +str('%'), font = font8, fill = 0) #Temp+Humidity
        draw.text((5, 39), str(artist)+str(' - ')+str(trackname), font = font14, fill = 0) #volumio zeug
        draw.text((5, 55), Uhrzeit, font = font24, fill = 0) #Uhrzeit

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()

if __name__ == '__main__':
    main()
