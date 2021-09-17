import time
import RPi.GPIO as GPIO
from encoder import Encoder
import pygame
from pygame import mixer

# keeps track of whether a person is standing on the scales or not
onToggle = False
# value at which scales register someone is standing on
boundaryValUp = 40
# value at which the second time it's seen, person is getting off
boundaryValDown = 60

# tracks how many people have stood on the scales
tracker = 0

GPIO.setmode(GPIO.BCM)
# setup GPIO pin to trigger relay (+ disco lamp)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
# setup GPIO pin to trigger relay (+ airbed pump with horn)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
# setup pin for shutdown button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# light up LED on startup
GPIO.setup(26, GPIO.OUT, initial=GPIO.HIGH)

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

import os

def Shutdown(channel):
    GPIO.cleanup()
    print("SHUTTING DOWN")
    os.system("sudo shutdown -h now")

# Shutdown function executes when button is pressed
GPIO.add_event_detect(16, GPIO.FALLING, callback=Shutdown, bouncetime=2000)

# function which runs whenever a the encoder moves
def valueChanged(value):
    print(value)
    if (value < 0):
        value = e1.resetValue()
    global onToggle
    global tracker
    global mixChannel
    if (value == boundaryValUp and onToggle == False):
        print("PERSON STEPPING ON")
        mixChannel = mixers[tracker].play()
        # disco ball on after 3rd person
        if (tracker > 2 and tracker <=4):
            GPIO.output(8, GPIO.HIGH)
        elif (tracker > 4 and tracker <=6):
            GPIO.output(7, GPIO.HIGH)
    elif (value == boundaryValDown and onToggle == False):
        onToggle = True
    elif (value == boundaryValDown and onToggle == True):
        print("PERSON STEPPING OFF")
        mixers[tracker].stop()
        if (tracker > 2 and tracker <=4):
            GPIO.output(8, GPIO.LOW)
        elif (tracker > 4 and tracker <=6):
            GPIO.output(7, GPIO.LOW)
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
            isPlaying = mixChannel.get_busy()
            print(isPlaying)
            # if track has finished
            if (not isPlaying):
                print("SCALES DIDN'T RESET PROPERLY... MOVING ON TO NEXT TRACK")
                # set pins to low
                GPIO.output(8, GPIO.LOW)
                GPIO.output(7, GPIO.LOW)
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