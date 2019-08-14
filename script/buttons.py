#!/usr/bin/python
# -*- coding:utf-8 -*-
print ('------------------------')
from datetime import datetime
import io
import sys
sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7 #lib fuer display
import epdconfig #config fuer display
from PIL import Image,ImageDraw,ImageFont
import subprocess, os
Datum = datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)

import time
epd = epd2in7.EPD()
epd.init()


key1 = 5
key2 = 6
key3 = 13
key4 = 19

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)



#schriftarten definieren
fontXXL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 107) # font for time
fontXL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 33) # font for date
fontL = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 29) # font for bday1
fontM = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 24) # font for volumio track ID
fontS = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 21) # font for bday2
fontXS = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 18) # font for temp, humi, cpu_temp


def updateDisplay(string):
    
    # Image with screen size
    #255: clear the image with white
    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)
    draw.text((5, 50), string, font = fontL, fill = 0)
    epd.display(epd.getbuffer(image))
 
def main():

    while True:
        
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            updateDisplay('Key1 pressed - Schlafzimmer on')
            print('Key1 Pressed - Schlafi on')
            os.system('/home/pi/hs100/hs100.sh on -i 192.168.0.227')
            time.sleep(0.2)
            
        if key2state == False:
            updateDisplay('Key2 pressed - Küche on')
            print('Key2 Pressed - Küche on')
            os.system('/home/pi/hs100/hs100.sh on -i 192.168.0.122')
            os.system('/home/pi/hs100/hs100.sh on -i 192.168.0.227')
            time.sleep(0.2)
           
        if key3state == False:
            updateDisplay('Key2 pressed - Wohnzimmer on')
            print('Key3 Pressed - Wohnzi on')
            os.system('/home/pi/hs100/hs100.sh on -i 192.168.0.38')
            os.system('/home/pi/hs100/hs100.sh on -i 192.168.0.227')
            time.sleep(0.2)
            
        if key4state == False:
            updateDisplay('Key2 pressed - Alles off geht noch nicht')
            print('Key4 Pressed - Alles off geht noch nich')
            time.sleep(0.2)
            
if __name__ == '__main__':
    main()
