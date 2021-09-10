# Sample code to demonstrate Encoder class.  Prints the value every 5 seconds, and also whenever it changes.

import time
import RPi.GPIO as GPIO
from encoder import Encoder

global pos = 0

def valueChanged(value):
    pos = value
    #print("* New value: {}".format(value))

GPIO.setmode(GPIO.BCM)

# 17 is the white wire, 18 is the green wire
e1 = Encoder(18, 17, valueChanged)

try:
    while True:
        print(pos)
        #print("Value is {}".format(e1.getValue()))
except Exception:
    pass

GPIO.cleanup()