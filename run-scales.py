import time
import RPi.GPIO as GPIO
from encoder import Encoder
from pygame import mixer

# keeps track of whether a person is standing on the scales or not
onToggle = False
boundaryVal = 40

# tracks how many people have stood on the scales
tracker = 0

GPIO.setmode(GPIO.BCM)
# setup GPIO pin to trigger relay (+ disco lamp)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# Initialize pygame mixer
mixer.init()

# Load the sounds
from os import listdir
from os.path import isfile, join
mypath = '/home/pi/Desktop/these-monsters-have-scales/sounds/'
sounds = [f for f in listdir(mypath) if isfile(join(mypath, f))]
mixers = []
# make array of mixers
for tracks in range(len(sounds)):
    mixers.append(mixer.Sound(f"{mypath}{sounds[tracks]}"))

def valueChanged(value):
    print(value)
    if (value < 0):
        value = e1.resetValue()
    global onToggle
    global tracker
    if (value == boundaryVal and onToggle == False):
        print("PERSON STEPPING ON")
        mixers[tracker].play()
        # disco ball on after 3rd person
        if (tracker > 2):
            GPIO.output(8, GPIO.HIGH)
        onToggle = True
    elif (value == boundaryVal and onToggle == True):
        print("PERSON STEPPING OFF")
        mixers[tracker].stop()
        if (tracker > 2):
            GPIO.output(8, GPIO.LOW)
        onToggle = False
        # reset back to 0 -> encoder not precise
        value = e1.resetValue()
        # track that 1 more person has stood on the scales
        tracker = tracker + 1

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