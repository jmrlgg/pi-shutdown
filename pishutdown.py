# shutdown/reboot(/power on) Raspberry Pi with pushbutton

import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime
import time

# pushbutton connected to this GPIO pin, using pin 5 also has the benefit of
# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 5

# if button pressed for at least this long then reboot. if less then shut down.
rebootMinSeconds = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None


def buttonStateChanged(pin):
    global buttonPressedTime

    if not (GPIO.input(pin)):
        # button is down
        buttonPressedTime = datetime.now()
    else:
        # button is up
        if buttonPressedTime is not None:
            if (datetime.now() - buttonPressedTime).total_seconds() >= rebootMinSeconds:
                # button pressed for more than specified time, reboot
                call(['shutdown', '-r', 'now'], shell=False)
            else:
                # button pressed for a shorter time, halt
                call(['shutdown', '-h', 'now'], shell=False)


# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonStateChanged)

while True:
    # sleep to reduce unnecessary CPU usage
    time.sleep(5)
