#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v2 by psw
print ('-----------------------------')
import io
f = open("/sys/class/thermal/thermal_zone0/temp", "r")
traw = f.readline ()
t = round(float(traw) / 1000)
import sys
sys.path.append(r'/home/pi/script/lib')
import epd2in7
import epdconfig
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
Datum = datetime.now().strftime('%d.%m.%Y')
Uhrzeit = datetime.now().strftime('%H:%M')

import thingspeak
ch = thingspeak.Channel(647418)
out = ch.get({'results':1})
outtruncTemp = out[465:470]
outtruncHumi = out[-60:-56]
print ('thingspeak: temp '+str(outtruncTemp)+'  humidity: '+str(outtruncHumi))


font24 = ImageFont.truetype('/home/pi/script/lib/Font.ttc', 98)
font18 = ImageFont.truetype('/home/pi/script/lib/Font.ttc', 34)
font8 = ImageFont.truetype('/home/pi/script/lib/Font.ttc', 14)
def main():
        #Init driver
        epd = epd2in7.EPD()
        print(Datum, Uhrzeit)
        print("init")
        epd.init()

        # Image with screen size
        #255: clear the image with white
        image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        #Object image on which we will draw
        draw = ImageDraw.Draw(image)

        #draw a rectangle in the center of the screen
        #draw.rectangle((epd2in7.EPD_WIDTH/2-10, epd2in7.EPD_HEIGHT/2-10, epd2in7.EPD_WIDTH/2+10, epd2in7.EPD_HEIGHT/2+10), fill = 0)

        draw.text((42, 0), Datum, font = font18, fill = 0)
        draw.text((0, 160), 'CPU: ' +str(t) +' °C', font = font8, fill = 0)
        draw.text((140, 160), str(outtruncTemp) +' °C     ' +str(outtruncHumi) +str(' %'), font = font8, fill = 0)

        draw.text((5, 60), Uhrzeit, font = font24, fill = 0)

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()

if __name__ == '__main__':
    main()
