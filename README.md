# waveshareEpaper

### multi purpose script for waveshare 2.7 inch black/white
short write up on https://peter-shaw.de/en/2019/07/diy-e-paper-display-with-raspberry-pi-zero-waveshare-e-paper-hat/


## implemented functions:
- pi temperature
- data from thingspeak channel
- calendar entries (see calendar.txt)
- date and time :)

## python scripts: 

- waveshare_uhr2.py: handles the main functions
- buttons.py: handles the 4 display buttons (switch wifi power outlets on/off)


## cronjob looks like this:
<code>crontab -e</code><br>
<code>
@reboot python3 /home/pi/script/waveshareEpaper/script/button.py > /home/pi/button.log 2>&1 &
* 7-8 * * * python3 /home/pi/script/waveshareEpaper/script/waveshare_uhr3.py > /dev/null 2>&1
0 9 * * * python3 /home/pi/script/waveshareEpaper/script/clean.py > /home/pi/clean.log 2>&1
* 17-21 * * * python3 /home/pi/script/waveshareEpaper/script/waveshare_uhr3.py > /dev/null 2>&1
0 22 * * * python3 /home/pi/script/waveshareEpaper/script/clean.py > /home/pi/clean.log 2>&1
</code>

