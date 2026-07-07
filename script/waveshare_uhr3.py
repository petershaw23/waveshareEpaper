#!/usr/bin/python
# -*- coding:utf-8 -*-
# uhr v3 (vereinfacht & robuster) by petershaw23 - zeigt Zeit, Datum, anstehenden
# Geburtstag, CPU-Temperatur sowie Temperatur/Luftfeuchte via ThingSpeak

import sys
from datetime import datetime, timedelta

import requests
from PIL import Image, ImageDraw, ImageFont

sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7  # lib fuer Display

LIB_PATH = '/home/pi/script/waveshareEpaper/lib'
FONT = f'{LIB_PATH}/Font.ttc'
BDAY_FILE = '/home/pi/script/waveshareEpaper/script/geburtstage.txt'
BDAY_LABELS = ("heute: ", "mrgn: ", "t-2: ", "t-3: ", "t-4: ")

CHANNELS = {
    "innen": 'https://api.thingspeak.com/channels/843073/feeds.json?results=1',
    "aussen": 'https://api.thingspeak.com/channels/647418/feeds.json?results=1',
}

REQUEST_TIMEOUT = 5  # Sekunden


def get_naechster_geburtstag(pfad):
    """Sucht die naechsten 0-4 Tage in geburtstage.txt nach einem Treffer."""
    daten = [(datetime.now() + timedelta(days=i)).strftime('%d.%m') for i in range(5)]

    with open(pfad, 'r') as f:
        zeilen = list(f)

    for tag_str, label in zip(daten, BDAY_LABELS):
        for zeile in zeilen:
            if zeile.startswith(tag_str):
                name = zeile.split(' ')[1].strip()
                return label, name
    return "", ""


def get_cpu_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return round(float(f.readline()) / 1000)


def get_thingspeak_temp_humi(url, humi_fallback=50):
    """Holt Temperatur (+ Platzhalter-Luftfeuchte) von einem ThingSpeak-Channel.
    Gibt bei Netzwerkfehlern "--"/"--" zurueck, damit das Display trotzdem laeuft."""
    try:
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        feed = data["feeds"][0]
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return "--", "--"

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
        return "err"


def main():
    now = datetime.now()
    datum = now.strftime('%-d.%-m.')
    uhrzeit = now.strftime('%H:%M')

    countdown, geb = get_naechster_geburtstag(BDAY_FILE)
    cpu_temp = get_cpu_temp()

    temp_innen, humi_innen = get_thingspeak_temp_humi(CHANNELS["innen"])
    temp_aussen, humi_aussen = get_thingspeak_temp_humi(CHANNELS["aussen"])

    delta_t = get_delta(temp_innen, temp_aussen)
    delta_h = get_delta(humi_innen, humi_aussen)

    print(f"{datum} {uhrzeit}")
    print(f"{countdown}{geb}")
    print(f"{cpu_temp}°C in: {temp_innen}°C {humi_innen}% "
          f"out: {temp_aussen}°C {humi_aussen}% Δt: {delta_t}°C ΔH: {delta_h}")

    # Schriftarten
    font_xxl = ImageFont.truetype(FONT, 107)  # Uhrzeit
    font_xl = ImageFont.truetype(FONT, 32)    # Datum
    font_xs = ImageFont.truetype(FONT, 17)    # CPU-Temp
    font_l2 = ImageFont.truetype(FONT, 29)    # Temp/Humi

    epd = epd2in7.EPD()
    epd.init()

    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)

    def text(x, y, s, font):
        draw.text((x, y), str(s), font=font, fill=0)

    text(0, -4, f"{datum} {countdown}{geb}", font_xl)
    draw.line((5, 33, 259, 33), fill=0)
    text(-4, 16, uhrzeit, font_xxl)
    draw.line((0, 125, 264, 125), fill=0)
    text(120, 80, cpu_temp, font_xs)
    text(0, 130, f"i:{temp_innen}°|{humi_innen}% o:{temp_aussen}°|{humi_aussen}", font_l2)

    epd.display(epd.getbuffer(image))
    epd.sleep()


if __name__ == '__main__':
    main()
