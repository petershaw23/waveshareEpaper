#manual calendar, to not be reliant on google api
import time 
import os 
  
# Birthday file is the one in which the actual birthdays 
# and dates are present. This file can be  
# manually edited or can be automated.  
# For simplicity, we will edit it manually. 
# Birthdays should be written in this file in 
# the format: "MonthDay Name Surname" (Without Quotes) 
  
birthdayFile = '/path/to/birthday/file'
  
def checkTodaysBirthdays(): 
    fileName = open(birthdayFile, 'r') 
    today = time.strftime('%m%d') 
    flag = 0
    for line in fileName: 
        if today in line: 
            line = line.split(' ') 
            flag =1
            # line[1] contains Name and line[2] contains Surname 
            print("Birthdays Today: ' + line[1]+ ' ' + line[2] + '"') 
    if flag == 0: 
            print("No Birthdays Today!"') 
  
if __name__ == '__main__': 
    checkTodaysBirthdays() 
