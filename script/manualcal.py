
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

count = 0

for line in fileName: 
    if today in line and count == 0: 
        line = line.split(' ') 
        gebToday = line[1]
        countdown = "heute: "
        print(str(countdown) + str(gebToday))
        count +=1
    if tomorrow in line and count == 0:
        line = line.split(' ')
        gebTomorrow = line[1]
        print("Birthday Tomorrow: " + gebTomorrow)
        count +=1
    if in2days in line and count == 0:
        line = line.split(' ')
        gebin2days = line[1]
        print("Birthday in 2 days: " + gebin2days)
        count +=1
    if in3days in line and count == 0:
        line = line.split(' ')
        gebin3days = line[1]
        print("Birthday in 3 days: " + gebin3days)
        count +=1
    if in4days in line and count == 0:
        line = line.split(' ')
        gebin4days = line[1]
        print("Birthday in 4 days: " + gebin4days)
        count +=1
        
print (count)


   
        
    
