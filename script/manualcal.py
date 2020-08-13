#manual calendar, to not be reliant on google api
import time 
import datetime
from dateutil import parser
Datum = datetime.datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)


List = open('geburtstage.txt').read().split(',')
print (List[0])
print (List[1])
print (List[2])
print (List[3])
