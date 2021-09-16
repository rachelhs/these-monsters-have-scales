import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW)

while True: # Run forever
    GPIO.output(8, GPIO.HIGH) # Turn on
    GPIO.output(7, GPIO.HIGH) # Turn on
    GPIO.output(5, GPIO.HIGH) # Turn on
    time.sleep(2)                  # Sleep for 2 seconds
    GPIO.output(8, GPIO.LOW)  # Turn off
    GPIO.output(7, GPIO.LOW) # Turn on
    GPIO.output(5, GPIO.LOW) # Turn on
    time.sleep(2)                  # Sleep for 2 seconds