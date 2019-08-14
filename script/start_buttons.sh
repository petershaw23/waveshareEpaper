#!/bin/bash
# u can call this file in crontab to execute the buttons script
# like so: 
# crontab -e 
# * * * * * /home/pi/script/waveshareEpaper/script/start_buttons.sh >> /home/pi/script/waveshareEpaper/buttons.txt 2>&1

#export DISPLAY=:0.0
source /home/pi/.profile
python3 /home/pi/script/waveshareEpaper/script/buttons.py
