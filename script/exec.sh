#!/bin/bash
# u can call this file in crontab to execute the main script
# like so: 
# crontab -e 
# * * * * * /home/pi/script/waveshareEpaper/script/exec.sh >> /home/pi/script/waveshareEpaper/clocklog2.txt 2>&1

export DISPLAY=:0.0
source /home/pi/.profile
python3 /home/pi/script/waveshareEpaper/script/waveshare_uhr3.py
