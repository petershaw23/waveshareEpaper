
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

in4daysRaw = datetime.now() + timedelta(days=4)
in4days = in4daysRaw.strftime('%d.%m') 

gebToday = " "
gebTomorrow = " "
gebin2days = " "
gebin3days = " "
gebin4days = " "
countdown = " "  

for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        gebToday = line[1]
        countdown = "heute: "
        print(str(countdown) + str(gebToday))
    if tomorrow in line:
        line = line.split(' ')
        gebTomorrow = line[1]
        print("Birthday Tomorrow: " + gebTomorrow)
    if in2days in line:
        line = line.split(' ')
        gebin2days = line[1]
        print("Birthday in 2 days: " + gebin2days)
    if in3days in line:
        line = line.split(' ')
        gebin3days = line[1]
        print("Birthday in 3 days: " + gebin3days)
    if in4days in line:
        line = line.split(' ')
        gebin4days = line[1]
        print("Birthday in 4 days: " + gebin4days)
        
  

   
        
    
