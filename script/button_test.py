import RPi.GPIO as GPIO

def getPinFunctionName(pin):
    functions = {GPIO.IN:'Input',
                 GPIO.OUT:'Output',
                 GPIO.I2C:'I2C',
                 GPIO.SPI:'SPI',
                 GPIO.HARD_PWM:'HARD_PWM',
                 GPIO.SERIAL:'Serial',
                 GPIO.UNKNOWN:'Unknown'}
                 
    return functions[GPIO.gpio_function(pin)]


gpio = (2,3,4,7,8,9,10,11,14,15,17,18,22,23,24,25,27)

GPIO.setmode(GPIO.BCM)
for pin in gpio:
    print("GPIO %s is an %s" % (pin,getPinFunctionName(pin)))
