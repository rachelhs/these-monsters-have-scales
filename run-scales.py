import time
import RPi.GPIO as GPIO
from encoder import Encoder
import os
from os import listdir
from os.path import isfile, join
import sys
from pathlib import Path
import signal
print("Starting scales", file=sys.stderr)

def exit_handler(*args):
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)
signal.signal(signal.SIGTERM, exit_handler)

# keeps track of whether a person is standing on the scales or not
onToggle = False
# value at which scales register someone is standing on
boundaryValUp = 40
# value at which the second time it's seen, person is getting off
boundaryValDown = 60

# tracks how many people have stood on the scales
tracker = 0

LED_PIN = 26
GPIO.setmode(GPIO.BCM)
# setup GPIO pin to trigger relay (+ disco lamp)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
# setup GPIO pin to trigger relay (+ airbed pump with horn)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
# setup GPIO pin to trigger relay (+ bubble machine)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
# setup pin for shutdown button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# light up LED on startup
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.HIGH)


import pygame
from pygame import mixer
# Initialize pygame mixer
mixer.init()

# Load the sounds
sound_root = Path('/home/pi/Desktop/these-monsters-have-scales/sounds/')
sound_paths = [p for p in sound_root.iterdir() if p.is_file()]
print(sound_paths)
mixers = [mixer.Sound(str(sound_path)) for sound_path in sound_paths]

def Shutdown(channel):
    GPIO.cleanup()
    print("SHUTTING DOWN", file=sys.stderr)
    os.system("sudo shutdown -h now")

# Shutdown function executes when button is pressed
GPIO.add_event_detect(16, GPIO.FALLING, callback=Shutdown, bouncetime=2000)

# function which runs whenever a the encoder moves
def valueChanged(value):
    print(value, file=sys.stderr)
    if (value < 0):
        value = e1.resetValue()
    global onToggle
    global tracker
    global mixChannel
    if (value == boundaryValUp and onToggle == False):
        print("PERSON STEPPING ON")
        mixChannel = mixers[tracker].play()
        # disco ball on for 3rd person
        if (tracker == 2):
            GPIO.output(8, GPIO.HIGH)
        # party horn for 5th person
        elif (tracker == 4):
            GPIO.output(7, GPIO.HIGH)
        # bubbles for 7th person
        elif (tracker == 6):
            GPIO.output(23, GPIO.HIGH)
        # disco for 9th person
        elif (tracker == 8):
            GPIO.output(8, GPIO.HIGH)
        # disco and horn for 11th person
        elif (tracker == 10):
            GPIO.output(8, GPIO.HIGH)
            GPIO.output(7, GPIO.HIGH)
    elif (value == boundaryValDown and onToggle == False):
        onToggle = True
    elif (value == boundaryValDown and onToggle == True):
        print("PERSON STEPPING OFF")
        mixers[tracker].stop()
        if (tracker == 2):
            GPIO.output(8, GPIO.LOW)
        elif (tracker == 4):
            GPIO.output(7, GPIO.LOW)
        elif (tracker == 6):
            GPIO.output(23, GPIO.LOW)
        elif (tracker == 8):
            GPIO.output(8, GPIO.LOW)
        elif (tracker == 10):
            GPIO.output(8, GPIO.LOW)
            GPIO.output(7, GPIO.LOW) 
        onToggle = False
        # reset back to 0 -> encoder not precise
        value = e1.resetValue()
        # track that 1 more person has stood on the scales
        if (tracker < (len(mixers) - 1)):
            tracker = tracker + 1
        # loop back to the beginning if at the end of the playlist
        else:
            tracker = 0

# 17 is the white wire, 18 is the green wire
e1 = Encoder(18, 17, valueChanged)

# run code on loop
print("Starting scale loop", file=sys.stderr)
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
            GPIO.output(23, GPIO.LOW)
            # reset value to 0
            value = e1.resetValue()
            # track that 1 more person has stood on the scales
            if (tracker < (len(mixers) - 1)):
                tracker = tracker + 1
            # loop back to the beginning if at the end of the playlist
            else:
                tracker = 0
            onToggle = False
