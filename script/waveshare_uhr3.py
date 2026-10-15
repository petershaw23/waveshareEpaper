#!/usr/bin/python
# -*- coding:utf-8 -*-
# uhr v4 by petershaw23 - zeigt Zeit, Datum, anstehenden Geburtstag,
# CPU-Temperatur, Ping/Uptime sowie Innen-/Aussentemperatur via ThingSpeak
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import requests
from PIL import Image, ImageDraw, ImageFont

LIB_PATH = '/home/pi/script/waveshareEpaper/lib'
sys.path.append(LIB_PATH)
import epd2in7  # lib fuer Display  # noqa: E402

FONT = f'{LIB_PATH}/Font.ttc'
BDAY_FILE = '/home/pi/script/waveshareEpaper/script/geburtstage.txt'
BDAY_LABELS = ("heute: ", "mrgn: ", "t-2: ", "t-3: ", "t-4: ")
WEB_DIR = "/tmp/uhr-web"

CHANNELS = {
    "innen": 'https://api.thingspeak.com/channels/843073/feeds.json?results=1',
    "aussen": 'https://api.thingspeak.com/channels/647418/feeds.json?results=1',
}

REQUEST_TIMEOUT = 5  # Sekunden
NA = "--"            # Platzhalter bei fehlenden Werten


def get_uptime():
    try:
        with open("/proc/uptime") as f:
            seconds = int(float(f.read().split()[0]))
    except (OSError, ValueError, IndexError):
        return NA

    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    return f"{days}d {hours}h" if days else f"{hours}h"


def get_ping():
    try:
        result = subprocess.check_output(
            ["ping", "-c", "1", "-W", str(REQUEST_TIMEOUT), "1.1.1.1"],
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=REQUEST_TIMEOUT + 2,
        )
        match = re.search(r"time[=<]([\d.]+)", result)
        if match:
            return f"{float(match.group(1)):.0f}ms"
    except (subprocess.SubprocessError, OSError, ValueError):
        pass
    return NA


def get_naechster_geburtstag(pfad, now):
    """Sucht die naechsten 0-4 Tage in geburtstage.txt nach einem Treffer."""
    daten = [(now + timedelta(days=i)).strftime('%d.%m') for i in range(5)]

    try:
        with open(pfad, 'r', encoding='utf-8') as f:
            zeilen = f.readlines()
    except OSError:
        return "", ""

    for tag_str, label in zip(daten, BDAY_LABELS):
        for zeile in zeilen:
            if zeile.startswith(tag_str):
                teile = zeile.split()
                if len(teile) > 1:
                    return label, teile[1]
    return "", ""


def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return round(float(f.readline()) / 1000)
    except (OSError, ValueError):
        return NA


def get_thingspeak_temp(url):
    """Holt die Temperatur (field2) von einem ThingSpeak-Channel.
    Gibt bei Fehlern NA zurueck, damit das Display trotzdem laeuft."""
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        feed = response.json()["feeds"][0]
        return round(float(feed["field2"]))
    except (requests.RequestException, KeyError, IndexError,
            TypeError, ValueError):
        return NA


def get_delta(a, b):
    try:
        return round(float(a) - float(b))
    except (TypeError, ValueError):
        return NA


def main():
    os.makedirs(WEB_DIR, exist_ok=True)
    now = datetime.now()
    datum = now.strftime('%-d.%-m.')
    uhrzeit = now.strftime('%H:%M')

    # Netzwerkabfragen parallel, damit sich die Timeouts nicht addieren
    with ThreadPoolExecutor(max_workers=3) as pool:
        f_ping = pool.submit(get_ping)
        f_innen = pool.submit(get_thingspeak_temp, CHANNELS["innen"])
        f_aussen = pool.submit(get_thingspeak_temp, CHANNELS["aussen"])
        ping = f_ping.result()
        temp_innen = f_innen.result()
        temp_aussen = f_aussen.result()

    uptime = get_uptime()
    countdown, geb = get_naechster_geburtstag(BDAY_FILE, now)
    cpu_temp = get_cpu_temp()
    delta_t = get_delta(temp_innen, temp_aussen)

    print(f"{datum} {uhrzeit}")
    print(f"{countdown}{geb}")
    print(f"{cpu_temp}°C in: {temp_innen}°C out: {temp_aussen}°C Δt: {delta_t}°C")

    # Schriftarten
    font_xxl = ImageFont.truetype(FONT, 107)  # Uhrzeit
    font_l = ImageFont.truetype(FONT, 32)     # Datum, Temperaturen
    font_xs = ImageFont.truetype(FONT, 17)    # CPU-Temp, Status

    image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(image)

    def text(x, y, s, font):
        draw.text((x, y), str(s), font=font, fill=0)

    text(0, -4, f"{datum} {countdown}{geb}", font_l)
    draw.line((5, 33, 259, 33), fill=0)
    text(-4, 16, uhrzeit, font_xxl)
    draw.line((0, 125, 264, 125), fill=0)
    text(120, 80, cpu_temp, font_xs)
    text(0, 130, f"i:{temp_innen}° o:{temp_aussen}°", font_l)

    # unten rechts: Ping + Uptime
    status = f"{ping} {uptime}"
    bbox = draw.textbbox((0, 0), status, font=font_xs)
    status_width = bbox[2] - bbox[0]
    text(264 - status_width - 4, 141, status, font_xs)

    image.save(f"{WEB_DIR}/uhr.png")

    epd = epd2in7.EPD()
    epd.init()
    try:
        epd.display(epd.getbuffer(image))
    finally:
        epd.sleep()


if __name__ == '__main__':
    main()
