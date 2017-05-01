#!/usr/bin/env python
# coding: latin-1

# Import libary functions we need
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import time

# Set which GPIO pins the drive outputs are connected to
DRIVE_1 = 4
DRIVE_2 = 18
DRIVE_3 = 8
DRIVE_4 = 7

# Set all of the drive pins as output pins
GPIO.setup(DRIVE_1, GPIO.OUT)
GPIO.setup(DRIVE_2, GPIO.OUT)
GPIO.setup(DRIVE_3, GPIO.OUT)
GPIO.setup(DRIVE_4, GPIO.OUT)

# Map the on/off state to nicer names for display
dName = {}
dName[True] = 'ON '
dName[False] = 'OFF'

# Function to set all drives off
def MotorOff():
    GPIO.output(DRIVE_1, GPIO.LOW)
    GPIO.output(DRIVE_2, GPIO.LOW)
    GPIO.output(DRIVE_3, GPIO.LOW)
    GPIO.output(DRIVE_4, GPIO.LOW)

# Setup for processor monitor
lProcessorFans = [DRIVE_1]                              # List of fans to turn on when processor is too hot
pathSensor = '/sys/class/thermal/thermal_zone0/temp'    # File path used to read the temperature
readingPrintMultiplier = 0.001                          # Value to multiply the reading by for user display
tempHigh = 50000                                        # Reading at which the fan(s) will be started (same units as file)
tempLow = 33000                                         # Reading at which the fan(s) will be stopped (same units as file)
interval = 1                                            # Time between readings in seconds

try:
    # Start by turning all drives off
    MotorOff()
    #raw_input('You can now turn on the power, press ENTER to continue')
    fansOn = False
    while True:
        # Read the temperature in from the file system
        fSensor = open(pathSensor, 'r')
        reading = float(fSensor.read())
        fSensor.close()
        # Adjust fan(s) depending on current status
        if fansOn:
            if reading <= tempLow:
                # We have cooled down enough, turn the fans off
                for fan in lProcessorFans:
                    GPIO.output(fan, GPIO.LOW)
                fansOn = False
        else:
            if reading >= tempHigh:
                # We have warmed up enough, turn the fans on
                for fan in lProcessorFans:
                    GPIO.output(fan, GPIO.HIGH)
                fansOn = True
        # Print the latest reading and the current state of all 4 drives
        print '%02.3f %s %s %s %s' % (reading * readingPrintMultiplier, dName[GPIO.input(DRIVE_1)], dName[GPIO.input(DRIVE_2)], dName[GPIO.input(DRIVE_3)], dName[GPIO.input(DRIVE_4)])
        # Wait a while
        time.sleep(interval)
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print 'Terminated'
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()

