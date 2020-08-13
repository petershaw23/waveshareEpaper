from datetime import datetime

with open('geburtstage.txt') as f:
    lines = [line.rstrip() for line in f]
    
print (lines)
lines_split = lines.split()
    
dates_list = [datetime.strptime(date, "%d.%m").date() for date in lines_split]
