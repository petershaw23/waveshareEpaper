import time
#manual calendar, to not be reliant on google api
fileName = open("geburtstage.txt", 'r') 
today = time.strftime('%m%d') 
flag = 0
for line in fileName: 
    if today in line: 
        line = line.split(' ') 
        flag = 1
        print("Birthdays Today: " + line[1]) 
    if flag == 0: 
        print("No Birthdays Today!") 
