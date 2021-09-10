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
boundaryVal = 10
# keeps track of whether person is stood on scales or not
onToggle = False

try:
        while True:
                # prevent negative values
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                # don't let counter go below 0
                                if (counter < 0):
                                    counter = 0
                                else:
                                    counter -= 1
                        if (counter == boundaryVal and onToggle == False):
                            onToggle = True
                            print("Person standing on")
                        elif (counter == boundaryVal and onToggle == True):
                            onToggle = False
                            print("Person getting off")
                            # set counter back to 0
                            counter = 0
                        print(counter)
                clkLastState = clkState
                sleep(0.01)
finally:
        GPIO.cleanup()