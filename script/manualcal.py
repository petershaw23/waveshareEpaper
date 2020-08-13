
from datetime import timedelta
from datetime import datetime

fileName = open("/home/pi/script/waveshareEpaper/script/geburtstage.txt", 'r') 
today = datetime.now().strftime('%d.%m')

tomorrowRaw = datetime.now() + timedelta(days=1)
tomorrow = tomorrowRaw.strftime('%d.%m') 

in2daysRaw = datetime.now() + timedelta(days=2)
in2days = in2daysRaw.strftime('%d.%m') 

flag = 0

for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        flag = 1
        gebToday = line[1]
        print("Birthdays Tomorrow: " + gebToday)
    if tomorrow in line:
        line = line.split(' ')
        flag = 2
        gebTomorrow = line[1]
        print("Birthdays Tomorrow: " + gebTomorrow)
    if in2days in line:
        line = line.split(' ')
        flag = 3
        gebin2days = line[1]
        print("Birthdays Tomorrow: " + gebin2days)
    if flag == 0:
        gebToday = " "
        gebTomorrow = " "
        gebin2days = " "
   
        
    
