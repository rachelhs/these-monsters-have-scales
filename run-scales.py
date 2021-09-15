import time
import RPi.GPIO as GPIO
from encoder import Encoder
import pygame
from pygame import mixer

# keeps track of whether a person is standing on the scales or not
onToggle = False
boundaryVal = 40

# tracks how many people have stood on the scales
tracker = 0

GPIO.setmode(GPIO.BCM)
# setup GPIO pin to trigger relay (+ disco lamp)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
# setup pin for shutdown button
GPIO.setup(16, GPIO.OUT, initial=GPIO.HIGH)

# Initialize pygame mixer
mixer.init()

# Load the sounds
from os import listdir
from os.path import isfile, join
mypath = '/home/pi/Desktop/these-monsters-have-scales/sounds/'
sounds = [f for f in listdir(mypath) if isfile(join(mypath, f))]
mixers = []
# count number of tracks
numberOfTracks = len(sounds)
# make array of mixers
for tracks in range(numberOfTracks):
    mixers.append(mixer.Sound(f"{mypath}{sounds[tracks]}"))

def Shutdown():
    print("SHUTTING DOWN")

# Shutdown function executes when button is pressed
GPIO.add_event_detect(16, GPIO.FALLING, callback=Shutdown, bouncetime=2000)

# function which runs whenever a the encoder moves
def valueChanged(value):
    print(value)
    if (value < 0):
        value = e1.resetValue()
    global onToggle
    global tracker
    global channel
    if (value == boundaryVal and onToggle == False):
        print("PERSON STEPPING ON")
        channel = mixers[tracker].play()
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
        if (tracker < (numberOfTracks - 1)):
            tracker = tracker + 1
        # loop back to the beginning if at the end of the playlist
        else:
            tracker = 0

# 17 is the white wire, 18 is the green wire
e1 = Encoder(18, 17, valueChanged)

# run code on loop
try:
    while True:
        time.sleep(5)
        # if song finishes and scales haven't reset properly - force reset and move on to next track
        if (onToggle):
            isPlaying = channel.get_busy()
            print(isPlaying)
            # if track has finished
            if (not isPlaying):
                print("SCALES DIDN'T RESET PROPERLY... MOVING ON TO NEXT TRACK")
                # set pins to low
                GPIO.output(8, GPIO.LOW)
                # reset value to 0
                value = e1.resetValue()
                # track that 1 more person has stood on the scales
                if (tracker < (numberOfTracks - 1)):
                    tracker = tracker + 1
                # loop back to the beginning if at the end of the playlist
                else:
                    tracker = 0
                onToggle = False

except Exception:
        pass

# reset pins before exit
GPIO.cleanup()