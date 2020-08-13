import time
import datetime
from datetime import timedelta

Datum = datetime.datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)


#manual calendar, to not be reliant on google api
fileName = open("/home/pi/script/waveshareEpaper/script/geburtstage.txt", 'r') 
today = time.strftime('%d.%m')
tomorrow = today + timedelta(days=1)  
print (tomorrow)
flag = 0
for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        flag = 1
        
        gebToday = line[1]
        print("Birthdays Today: " + gebToday)
    if flag == 0:
        gebToday = " "
        print(gebToday) 
    
