from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
import gcallite2
geb = gcallite2.geb
list = gcallite2.list
print (list)
print (geb)
print ('-------------')
next_geb = list[0]
print (next_geb)
next_geb_dateRaw = (next_geb[0])
next_geb_name = (next_geb[1])
next_geb_date = datetime.strptime(next_geb_dateRaw, '%Y-%m-%d')
deltaRaw = next_geb_date - datetime.now()
delta = (deltaRaw.days + 1)
print (delta)
