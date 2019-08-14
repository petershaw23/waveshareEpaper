import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def main():

    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            print('Key1 Pressed')
            time.sleep(0.2)
        if key2state == False:
            print('Key2 Pressed')
            time.sleep(0.2)
        if key3state == False:
            print('Key3 Pressed')
            time.sleep(0.2)
        if key4state == False:
            print('Key4 Pressed')
            updateDisplay('Key4 pressed')
            time.sleep(0.2)

if __name__ == '__main__':
    main()
