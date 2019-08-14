import thingspeak
try:
    chPi1 = thingspeak.Channel(647418)
    outRAWPi1 = chPi1.get({'results':1})
    outSplitPi1 = outRAWPi1.split('\"')
    outTempPi1 = outSplitPi1[-18]
    outHumiPi1 = outSplitPi1[-14]

    chD1 = thingspeak.Channel(843073)
    outRAWD1 = chD1.get({'results':1})
    outSplitD1 = outRAWD1.split('\"')
    outTempD1 = outSplitD1[-14]
    outHumiD1 = outSplitD1[-10]
    
    deltaT = round(float(outTempPi1) - float(outTempD1), 3)
    deltaH = round(float(outHumiPi1) - float(outHumiD1), 3)

except: #falls offline
    outTempPi1 = 'err'
    outHumiPi1 = 'err'
    outTempD1 = 'err'
    outHumiD1 = 'err'
    deltaT = 'err'
    deltaH = 'err'

print ('out: '+str(outTempD1)+'°C  '+str(outHumiD1)+str('%    in: ')+str(outTempPi1)+'°C  '+str(outHumiPi1)+str('%    Delta t: ' )+str(deltaT)+str('°C   Delta H: ' )+str(deltaH))
