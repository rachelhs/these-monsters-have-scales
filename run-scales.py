import time
import RPi.GPIO as GPIO
from encoder import Encoder
from pygame import mixer

# keeps track of whether a person is standing on the scales or not
onToggle = False
boundaryVal = 80

GPIO.setmode(GPIO.BCM)
# setup GPIO pin to trigger relay (+ disco lamp)
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)

# Initialize pygame mixer
mixer.init()

# Load the sounds
sound = mixer.Sound('home/pi/Desktop/these-monsters-have-scales/sounds/Respect.mp3')

def valueChanged(value):
    print(value)
    if (value < 0):
        value = e1.resetValue()
    global onToggle
    if (value == boundaryVal and onToggle == False):
        print("PERSON STEPPING ON")
        sound.play()
        GPIO.output(13, GPIO.HIGH)
        onToggle = True
    elif (value == boundaryVal and onToggle == True):
        print("PERSON STEPPING OFF")
        onToggle = False
        GPIO.output(13, GPIO.LOW)
        # reset back to 0 -> encoder not precise
        value = e1.resetValue()

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