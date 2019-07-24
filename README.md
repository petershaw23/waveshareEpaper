# waveshareEpaper
multi purpose script for waveshare 2.7 inch black/white

implemented functions:
- pi temperature
- data from thingspeak channel
- track ID from volumio REST API (= multi room audio player, in the same network)
- calendar entries from google calendar API
- date and time :)

2 python scripts: 

- waveshare_uhr2.py: handles the main functions
- gcallite.py: handles google calendar API

google calendar api needs to be authed via browser at the first run. use "exec.sh" to run via cronjob (correct enviroment settings). 

cronjob looks like this:
<code>crontab -e</code><br>
<code>* * * * * /home/pi/script/waveshareEpaper/script/exec.sh >> /home/pi/script/waveshareEpaper/clocklog2.txt 2>&1</code>
