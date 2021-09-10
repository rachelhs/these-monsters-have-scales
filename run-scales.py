from RPi import GPIO
from time import sleep

# white wire
clk = 17
# green wire
dt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

# above this value is person getting on scales, below is person getting off
boundaryVal = 80

try:
        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        if (counter == boundaryVal):
                            print("ACTION")
                        print(counter)
                clkLastState = clkState
                sleep(0.01)
finally:
        GPIO.cleanup()