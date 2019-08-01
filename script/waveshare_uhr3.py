#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v3 by petershaw23 - shows time, date, google calendar current bday, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('-----------------------------')
from datetime import datetime
Datum = datetime.now().strftime('%d.%m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)
# google API get bdays
try:
    import gcallite2 #imports gcallite2.py from same directory. if this script is executed via cronjob, check env. settings! or use attached bash file "exec.sh" to oauth instead
    geb = gcallite2.geb #call variable from imported file
    list = gcallite2.list #call list from imported file
    next_geb = list[0] #the first list entry
    #print (next_geb)
    next_geb_dateRaw = (next_geb[0])
    next_geb_name = (next_geb[1])
    next_geb_date = datetime.strptime(next_geb_dateRaw, '%Y-%m-%d')
    deltaRaw = next_geb_date - datetime.now()
    delta = (deltaRaw.days + 1)
    #print ('next bday in '+str(delta)+str(' days: ')+str(next_geb_name))
    if geb == str(' '): #if there is no bday today
        geb = ('in ' +str(delta) +'T: ' +str(next_geb_name))
except: #falls fehler
    geb = 'error'
    geb_next = 'error'
    delta = '?'
print ('heute: '+str(geb))
print ('in ' +str(delta) +'T: ' +str(next_geb))
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
        #draw.text((5, 23), str(geb_next)+str(' hat in ')+str(delta)+str(' Tagen bday!'), font = font8, fill = 0) #next bday
        draw.text((158, 160), str(outTemp) +'°C    ' +str(outHumi) +str('%'), font = font8, fill = 0) #Temp+Humidity
        draw.text((5, 39), str(artist)+str(' - ')+str(trackname), font = font14, fill = 0) #volumio track ID
        draw.text((5, 55), Uhrzeit, font = font24, fill = 0) #time

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()

if __name__ == '__main__':
    main()

