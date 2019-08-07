#!/bin/bash
# script to take webcam pic and send to remote server
# dependency: fswebcam (sudo apt-get install fswebcam)
# this script gets called by the main script waveshare_uhr.py

source /home/pi/.profile
fswebcam -d /dev/video0 -r 352x288 test.jpeg
scp test.jpeg hosting126791@188.68.47.235:httpdocs/peter-shaw/
echo "webcam pic uploaded to remote server"
