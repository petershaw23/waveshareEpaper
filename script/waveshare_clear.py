#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append(r'/home/pi/script/lib')
import time
import epd2in7
import epdconfig
from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
Datum = datetime.now().strftime('%d.%m.%Y')
Uhrzeit = datetime.now().strftime('%H:%M')
time.sleep(20)


def main():
        #Init driver
        epd = epd2in7.EPD()
        print("clean script 1 mal pro tag")
        print(Datum, Uhrzeit)
        print("init")
        epd.init()
        epd.Clear(0XFF)
       

        print("Goto Sleep...")
        epd.sleep()

if __name__ == '__main__':
    main()
