#!/usr/bin/python
# -*- coding:utf-8 -*-
# uhr v3 (vereinfacht) by petershaw23 - zeigt Zeit, Datum, anstehenden Geburtstag,
# CPU-Temperatur sowie Temperatur/Luftfeuchte via ThingSpeak

import sys
import json
from datetime import datetime, timedelta

import requests
from PIL import Image, ImageDraw, ImageFont

sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7  # lib fuer Display

LIB_PATH = '/home/pi/script/waveshareEpaper/lib'
BDAY_FILE = '/home/pi/script/waveshareEpaper/script/geburtstage.txt'

THINGSPEAK_PI1 = 'https://api.thingspeak.com/channels/843073/feeds.json?results=1'
THINGSPEAK_D1 = 'https://api.thingspeak.com/channels/647418/feeds.json?results=1'


def get_naechster_geburtstag(pfad):
    """Sucht die naechsten 0-4 Tage in geburtstage.txt nach einem Treffer."""
    labels = ["heute: ", "mrgn: ", "t-2: ", "t-3: ", "t-4: "]
    daten = [(datetime.now() + timedelta(days=i)).strftime('%d.%m') for i in range(5)]

    with open(pfad, 'r') as f:
        zeilen = f.readlines()

    for tag_str, label in zip(daten, labels):
        for zeile in zeilen:
            if tag_str in zeile:
                name = zeile.split(' ')[1].strip()
                return label, name
    return "", ""


def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return round(float(f.readline()) / 1000)


def get_thingspeak_temp_humi(url, humi_fallback=50):
    """Holt Temperatur (+ Platzhalter-Luftfeuchte) von einem ThingSpeak-Channel."""
    data = requests.get(url=url).json()
    feed = data["feeds"][0]
    try:
        temp = round(float(feed["field2"]))
        humi = humi_fallback
    except (TypeError, ValueError):
        temp = feed.get("field1")
        humi = feed.get("field2")
    return temp, humi


def get_delta(a, b):
    try:
        return round(float(a) - float(b))
    except (TypeError, ValueError):
        return 'err'


def main():
    datum = datetime.now().strftime('%-d.%-m.')
    uhrzeit = datetime.now().strftime('%H:%M')

    countdown, geb = get_naechster_geburtstag(BDAY_FILE)
    cpu_temp = get_cpu_temp()

    temp_innen, humi_innen = get_thingspeak_temp_humi(THINGSPEAK_PI1)
    temp_aussen, humi_aussen = get_thingspeak_temp_humi(THINGSPEAK_D1)

    delta_t = get_delta(temp_innen, temp_aussen)
    delta_h = get_delta(humi_innen, humi_aussen)

    print(f"{datum} {uhrzeit}")
    print(f"{countdown}{geb}")
    print(f"{cpu_temp}°C in: {temp_innen}°C {humi_innen}% "
          f"out: {temp_aussen}°C {humi_aussen}% Δt: {delta_t}°C ΔH: {delta_h}")

    # Schriftarten
    font_xxl = ImageFont.truetype(f'{LIB_PATH}/Font.ttc', 107)  # Uhrzeit
    font_xl = ImageFont.truetype(f'{LIB_PATH}/Font.ttc', 32)    # Datum
    font_xs = ImageFont.truetype(f'{LIB_PATH}/Font.ttc', 17)    # CPU-Temp
    font_l2 = ImageFont.truetype(f'{LIB_PATH}/Font.ttc', 29)    # Temp/Humi

    epd = epd2in7.EPD()
    epd.init()

    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)

    draw.text((0, -4), f"{datum} {countdown}{geb}", font=font_xl, fill=0)
    draw.line((5, 33, 259, 33), fill=0)
    draw.text((-4, 16), uhrzeit, font=font_xxl, fill=0)
    draw.line((0, 125, 264, 125), fill=0)
    draw.text((120, 80), str(cpu_temp), font=font_xs, fill=0)
    draw.text((0, 130), f"i:{temp_innen}°|{humi_innen}% o:{temp_aussen}°|{humi_aussen}",
               font=font_l2, fill=0)

    epd.display(epd.getbuffer(image))
    epd.sleep()


if __name__ == '__main__':
    main()
