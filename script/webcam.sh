#!/bin/bash

source /home/pi/.profile
fswebcam -d /dev/video0 -r 352x288 test.jpeg
scp test.jpeg hosting126791@188.68.47.235:httpdocs/peter-shaw/
