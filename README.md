# waveshareEpaper

### multi purpose script for waveshare 2.7 inch black/white
short write up on https://michaelbudjan.de/en/2019/07/diy-e-paper-display-with-raspberry-pi-zero-waveshare-e-paper-hat/


## implemented functions:
- pi temperature
- data from thingspeak channel
- track ID from volumio REST API (= multi room audio player, in the same network)
- calendar entries from google calendar API
- date and time :)

## python scripts: 

- waveshare_uhr2.py: handles the main functions
- gcallite.py: handles google calendar API
- buttons.py: handles the 4 display buttons (switch wifi power outlets on/off)


## display layout (webcam pic):

![alt text](https://peter-shaw.de/waveshare.jpg "layout")


## google calendar api 
api needs to be authed via browser at the first run. use "exec.sh" to run via cronjob (correct enviroment settings). 

## cronjob looks like this:
<code>crontab -e</code><br>
<code>* * * * * /home/pi/script/waveshareEpaper/script/exec.sh >> /home/pi/script/waveshareEpaper/clocklog2.txt 2>&1</code>

## to-do
- maps.py: google maps API, outputs time till next train is coming
