
from datetime import timedelta
from datetime import datetime

fileName = open("/home/pi/script/waveshareEpaper/script/geburtstage.txt", 'r') 
today = datetime.now().strftime('%d.%m')

tomorrowRaw = datetime.now() + timedelta(days=1)
tomorrow = tomorrowRaw.strftime('%d.%m') 

in2daysRaw = datetime.now() + timedelta(days=2)
in2days = in2daysRaw.strftime('%d.%m') 

in3daysRaw = datetime.now() + timedelta(days=3)
in3days = in3daysRaw.strftime('%d.%m') 

flag = 0

for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        flag = 1
        gebToday = line[1]
        print("Birthday Today: " + gebToday)
    if tomorrow in line:
        line = line.split(' ')
        flag = 2
        gebTomorrow = line[1]
        print("Birthday Tomorrow: " + gebTomorrow)
    if in2days in line:
        line = line.split(' ')
        flag = 3
        gebin2days = line[1]
        print("Birthday in 2 days: " + gebin2days)
    if in3days in line:
        line = line.split(' ')
        flag = 4
        gebin3days = line[1]
        print("Birthday in 3 days: " + gebin3days)
        
    if flag == 0:
        gebToday = " "
        gebTomorrow = " "
        gebin2days = " "
        gebin3days = " "
   
        
    
