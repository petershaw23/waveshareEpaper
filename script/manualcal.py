#manual calendar, to not be reliant on google api
import time 
  
birthdayFile = 'geburtstage.txt'
  
def checkTodaysBirthdays(): 
    fileName = open(birthdayFile, 'r') 
    today = time.strftime('%m%d') 
    flag = 0
    for line in fileName: 
        if today in line: 
            line = line.split(' ') 
            flag =1
            # line[1] contains Name and line[2] contains Surname 
            print("Birthdays Today: " + line[1]) 
    if flag == 0: 
            print("No Birthdays Today!") 
  
if __name__ == '__main__': 
    checkTodaysBirthdays() 
