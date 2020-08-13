#manual calendar, to not be reliant on google api
import time 
Datum = datetime.datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)
List = open("geburtstage.txt").readlines()
next_geb = List[0] #the first list entry
print (next_geb)
next_geb_dateRaw = (next_geb[0])
next_geb_name = (next_geb[1])
next_geb_date = datetime.datetime.strptime(next_geb_dateRaw, '%Y-%m-%d')
deltaRawNext = next_geb_date - datetime.datetime.now()
deltaNext = (deltaRawNext.days + 1)
print (next_geb_dateRaw)
print (next_geb_name)
print (deltaRawNext)
print (deltaNext)
#            gebStringNext = ('t-' +str(deltaNext) +': ' +str(next_geb_name)) 
#    except:
#        gebStringNext = (' ')
#    try:
#        uebernext_geb = list[1] #the next after the first one
#        uebernext_geb_dateRaw = (uebernext_geb[0])
#        uebernext_geb_name = (uebernext_geb[1])
#        uebernext_geb_date = datetime.datetime.strptime(uebernext_geb_dateRaw, '%Y-%m-%d')
#        deltaRawUeberNext = uebernext_geb_date - datetime.datetime.now()
#        deltaUeberNext = (deltaRawUeberNext.days + 1)
#        if deltaUeberNext == 1:
#            gebStringUeberNext = ('mrgn: '+str(uebernext_geb_name))
#        else:
#            gebStringUeberNext = ('t-'+str(deltaUeberNext)+': '+str(uebernext_geb_name))
#    except:
#        gebStringUeberNext = (' ')
#
#except: #falls fehler
#    gebStringNext = '--'
#    gebStringUeberNext = '--'
#print (gebStringNext)
#print (gebStringUeberNext)
###
