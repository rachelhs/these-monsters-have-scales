import time
import RPi.GPIO as GPIO
from encoder import Encoder

# keeps track of whether a person is standing on the scales or not
onToggle = False
boundaryVal = 80

def valueChanged(value):
    print(value)
    if (value == boundaryVal and onToggle == False):
        print("PERSON STEPPING ON")
        onToggle = True
    elif (value == boundaryVal and onToggle == True):
        print("PERSON STEPPING OFF")
        onToggle = False

GPIO.setmode(GPIO.BCM)

# 17 is the white wire, 18 is the green wire
e1 = Encoder(18, 17, valueChanged)

# run code on loop
try:
    while True:
        time.sleep(5)
except Exception:
        pass

# reset pins before exit
GPIO.cleanup()