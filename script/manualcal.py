#manual calendar, to not be reliant on google api
import time 
import datetime
from dateutil import parser
Datum = datetime.datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)


List = open('geburtstage.txt').read().split(',')
next_geb = List[0] #the first list entry
print (next_geb)
next_geb_dateRaw = (next_geb[0])
next_geb_name = (next_geb[1])
#next_geb_date = datetime.datetime.strptime(next_geb_dateRaw, '%Y-%m-%d')
#deltaRawNext = next_geb_date - datetime.datetime.now()
#deltaNext = (deltaRawNext.days + 1)
print (next_geb_dateRaw)
print (next_geb_name)
#print (deltaRawNext)
#print (deltaNext)
