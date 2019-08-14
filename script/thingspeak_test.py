###
# temperatur und humidity von thingspeak channel holen
try:
    chPi1 = thingspeak.Channel(647418)
    outRAWPi1 = chPi1.get({'results':1})
    chD1 = thingspeak.Channel(843073)
    outRAWD1 = chD1.get({'results':1})
except: #falls offline
    outTempPi1 = 'off'
    outHumiPi1 = 'off'
    outTempD1 = 'off'
    outHumiD1 = 'off'
    deltaT = 'off'
    deltaH = 'off'    
    
outSplitPi1 = outRAWPi1.split('\"')
try:
    outTempPi1 = outSplitPi1[-18]
except:
    outTempPi1 = 'err'
    
try:
    outHumiPi1 = outSplitPi1[-14]
except:
    outHumiPi1 = 'err'
   
outSplitD1 = outRAWD1.split('\"')
    
try:
    outTempD1 = outSplitD1[-14]
except:
    outTempD1 = 'err'
try:
    outHumiD1 = outSplitD1[-10]
except: 
    outTempD1 = 'err'
    
try:
    deltaT = round(float(outTempPi1) - float(outTempD1), 2)
    deltaH = round(float(outHumiPi1) - float(outHumiD1), 2)
except:
    deltaT = 'err'
    deltaH = 'err'


print ('out: '+str(outTempD1)+'°C  '+str(outHumiD1)+str('%    in: ')+str(outTempPi1)+'°C  '+str(outHumiPi1)+str('%    Delta t: ' )+str(deltaT)+str('°C   Delta H: ' )+str(deltaH))
