#!/usr/bin/env python3

import RPi.GPIO as GPIO
import subprocess
import time
from datetime import datetime
print(f"{datetime.now():%Y-%m-%d %H:%M:%S} button.py gestartet", flush=True)
# GPIO-Pins der 4 Tasten
KEY1 = 5
KEY2 = 6
KEY3 = 13
KEY4 = 19

GPIO.setmode(GPIO.BCM)

for key in [KEY1, KEY2, KEY3, KEY4]:
    GPIO.setup(key, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def refresh_display():
    subprocess.Popen([
        "python3",
        "/home/pi/script/waveshareEpaper/script/waveshare_uhr3.py"
    ])

def clean_display():
    subprocess.Popen([
        "python3",
        "/home/pi/script/waveshareEpaper/script/clean.py"
    ])

try:
    while True:

        if GPIO.input(KEY1) == 0:
            refresh_display()
            time.sleep(0.5)

        if GPIO.input(KEY2) == 0:
            refresh_display()
            time.sleep(0.5)

        if GPIO.input(KEY3) == 0:
            refresh_display()
            time.sleep(0.5)

        if GPIO.input(KEY4) == 0:
            clean_display()
            time.sleep(7)

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
