
from datetime import timedelta
from datetime import datetime

fileName = open("/home/pi/script/waveshareEpaper/script/geburtstage.txt", 'r') 
today = time.strftime('%d.%m')
tomorrowRaw = datetime.now() + timedelta(days=1) 
tomorrow = tomorrowRaw.strftime('%d.%m') 
print (today)
print (tomorrow)
flag = 0
for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        flag = 1
    if tomorrow in line:
        line = line.split(' ')
        flag = 2
        gebTomorrow = line[1]
        print("Birthdays Tomorrow: " + gebTomorrow)
    if flag == 0:
        gebToday = " "
        gebTomorrow = " "
        print(gebToday)
        
    
