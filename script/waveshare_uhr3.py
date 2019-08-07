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
    list = gcallite2.list #call list from imported file
    
    try:
        next_geb = list[0] #the first list entry
        next_geb_dateRaw = (next_geb[0])
        next_geb_name = (next_geb[1])
        next_geb_date = datetime.strptime(next_geb_dateRaw, '%Y-%m-%d')
        deltaRawNext = next_geb_date - datetime.now()
        deltaNext = (deltaRawNext.days + 1)
        if deltaNext == 0:
            gebStringNext = str(next_geb_name)+str('!')
        elif deltaNext == 1:
            gebStringNext = ('morgen: '+str(next_geb_name))
        else:
            gebStringNext = ('in ' +str(deltaNext) +'T: ' +str(next_geb_name)) 
    except:
        gebStringNext = ('no bday in next week')
    try:
        uebernext_geb = list[1] #the next after the first one
        uebernext_geb_dateRaw = (uebernext_geb[0])
        uebernext_geb_name = (uebernext_geb[1])
        uebernext_geb_date = datetime.strptime(uebernext_geb_dateRaw, '%Y-%m-%d')
        deltaRawUeberNext = uebernext_geb_date - datetime.now()
        deltaUeberNext = (deltaRawUeberNext.days + 1)
        if deltaUeberNext == 1:
            gebStringUeberNext = ('morgen: '+str(uebernext_geb_name))
        else:
            gebStringUeberNext = ('in ' +str(deltaUeberNext) +'T: ' +str(uebernext_geb_name))
    except:
        gebStringUeberNext = ('no further bday in next week')

except: #falls fehler
    gebStringNext = 'error in gcallite.py'
    gebStringUeberNext = 'error in gcallite.py'
print (gebStringNext)
print (gebStringUeberNext)
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



# track ID via volumio REST api holen:
import subprocess, os
trackid = subprocess.Popen("curl 192.168.0.241/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputRAW, error) = trackid.communicate()
if trackid.returncode != 0: #if offline
   artist = ' '
   trackname = ' '
   trackIDString = 'Volumio Offline'
else:
   trackname = outputRAW.decode().split('\"')[9]
   artist = outputRAW.decode().split('\"')[13]
   trackIDString = (str(artist)+str(' - ')+str(trackname))
   #albumart = outputRAW.decode().split('\"')[21] #das waere sau cool

print (trackIDString)
######################################################################################################
#schriftarten definieren
fontXXL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 105) # font for time
fontXL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 33) # font for date
fontL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 30) # font for bday1
fontM = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 25) # font for volumio track ID
fontS = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 22) # font for bday2
fontXS = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 15) # font for temp, humi, cpu_temp
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
        draw.text((0, -7), Datum, font = fontXL, fill = 0)              # Date
        draw.text((98, -7), gebStringNext, font = fontL, fill = 1)     # bday1
        draw.text((0, 23), gebStringUeberNext, font = fontS, fill = 0) #bday2
        draw.line((0, 50, 264, 50), fill = 0)
        #draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        #draw.rectangle((10, 150, 60, 200), fill = 0)
        #draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        draw.text((0, 49), trackIDString, font = fontM, fill = 0)       # volumio track ID
        draw.line((0, 78, 264, 78), fill = 0)
        draw.text((0, 58), Uhrzeit, font = fontXXL, fill = 0)           # time
        draw.line((0, 162, 264, 162), fill = 0)
        draw.text((0, 161), str(t) +' °C', font = fontXS, fill = 0)       #CPU temp
        draw.text((158, 161), str(outTemp) +'°C    ' +str(outHumi) +str('%'), font = fontXS, fill = 0) # Temp+Humidity

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()
        # webcam pic to remote server (useful for layout adjustment if waveshare display is not in the same room)
        #p = subprocess.Popen(["pwd"], stdout=subprocess.PIPE) # to check current directory
        #out = p.stdout.read()
        #print (out)
        p2 = subprocess.Popen(["script/waveshareEpaper/script/webcam.sh"], stdout=subprocess.PIPE)
        out2 = p2.stdout.read()
        #print (out2) #for debugging of the webcam.sh script

if __name__ == '__main__':
    main()

