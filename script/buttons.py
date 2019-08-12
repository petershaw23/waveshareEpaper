#import epd2in7
#import Image
#import ImageFont
#import ImageDraw

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

#epd = epd2in7.EPD()
#epd.init()
#image = Image.new('1', (epd2in7.EPD_WIDTH, epd2in7.EPD_HEIGHT), 255)    # 255: clear the image with white

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def updateDisplay(string):

    #draw = ImageDraw.Draw(image)
    #font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

    #draw.text((20, 50), string, font = font, fill = 0)
    #draw.rectangle((epd2in7.EPD_WIDTH/2-10, epd2in7.EPD_HEIGHT/2-10, epd2in7.EPD_WIDTH/2+10, epd2in7.EPD_HEIGHT/2+10), fill = 0)
    print('update display')
    #epd.display_frame(epd.get_frame_buffer(image))

def main():

    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            print('Key1 Pressed')
            time.sleep(0.2)
        if key2state == False:
            print('Key2 Pressed')
            time.sleep(0.2)
        if key3state == False:
            print('Key3 Pressed')
            time.sleep(0.2)
        if key4state == False:
            print('Key4 Pressed')
            #updateDisplay('Key4 pressed')
            time.sleep(0.2)

if __name__ == '__main__':
    main()
