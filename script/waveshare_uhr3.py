#!/usr/bin/python
# -*- coding:utf-8 -*-
# uhr v3 (vereinfacht & robuster) by petershaw23 - zeigt Zeit, Datum, anstehenden
# Geburtstag, CPU-Temperatur sowie Temperatur/Luftfeuchte via ThingSpeak
import os
os.makedirs("/tmp/uhr-web", exist_ok=True)

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
import subprocess
import re

def get_uptime():
    with open("/proc/uptime") as f:
        seconds = int(float(f.read().split()[0]))

    days = seconds // 86400
    hours = (seconds % 86400) // 3600

    if days:
        return f"{days}d {hours}h"
    else:
        return f"{hours}h"
        
def get_ping():
    try:
        result = subprocess.check_output(
            ["ping", "-c", "1", "-W", "5", "1.1.1.1"],
            stderr=subprocess.DEVNULL,
            text=True
        )

        match = re.search(r"time[=<]([\d.]+)", result)
        if match:
            return f"{float(match.group(1)):.0f}ms"

    except:
        pass

    return "--"

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


def get_thingspeak_temp(url):
    """Holt die Temperatur von einem ThingSpeak-Channel.
    Gibt bei Netzwerkfehlern "--" zurueck, damit das Display trotzdem laeuft."""
    try:
        data = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        feed = data["feeds"][0]
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return "--"

    try:
        return round(float(feed["field2"]))
    except (TypeError, ValueError):
        return "--"


def get_delta(a, b):
    try:
        return round(float(a) - float(b))
    except (TypeError, ValueError):
        return "err"


def main():
    ping = get_ping()
    uptime = get_uptime()
    now = datetime.now()
    datum = now.strftime('%-d.%-m.')
    uhrzeit = now.strftime('%H:%M')

    countdown, geb = get_naechster_geburtstag(BDAY_FILE)
    cpu_temp = get_cpu_temp()

    temp_innen = get_thingspeak_temp(CHANNELS["innen"])
    temp_aussen = get_thingspeak_temp(CHANNELS["aussen"])

    delta_t = get_delta(temp_innen, temp_aussen)

    print(f"{datum} {uhrzeit}")
    print(f"{countdown}{geb}")
    print(f"{cpu_temp}°C in: {temp_innen}°C out: {temp_aussen}°C Δt: {delta_t}°C")

    # Schriftarten
    font_xxl = ImageFont.truetype(FONT, 107)  # Uhrzeit
    font_xl = ImageFont.truetype(FONT, 32)    # Datum
    font_xs = ImageFont.truetype(FONT, 17)    # CPU-Temp
    font_l2 = ImageFont.truetype(FONT, 32)    # Temp/Humi

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
    text(0, 130, f"i:{temp_innen}° o:{temp_aussen}°", font_l2)
    
     # unten rechts: Ping + Uptime
    status = f"{ping} {uptime}"
    bbox = draw.textbbox((0, 0), status, font=font_xs)
    status_width = bbox[2] - bbox[0]
    text(264 - status_width - 4, 141, status, font_xs)
    
    image.save("/tmp/uhr-web/uhr.png")
    epd.display(epd.getbuffer(image))
    epd.sleep()


if __name__ == '__main__':
    main()
