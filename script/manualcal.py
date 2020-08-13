import time
#manual calendar, to not be reliant on google api
fileName = open("geburtstage.txt", 'r') 
today = time.strftime('%d.%m')
flag = 0
for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        flag = 1
        
        gebToday = line[1]
        print("Birthdays Today: " + gebToday)
    if flag == 0:
        gebToday = "No Birthdays Today!"
        print(gebToday) 
