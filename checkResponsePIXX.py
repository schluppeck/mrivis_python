#! /usr/bin/env python
"""
checkResponsePIXX.py

This script is a simple example of how to use the DATAPixx3 with PsychoPy.

Small elaborations of original code from:

https://www.vpixx.com/manuals/python/html/basicdemo.html#example-8-how-to-read-button-presses-from-a-responsepixx

"""
import psychopy
from psychopy import visual, core, event, gui, plugins
import sys
import argparse
import time
import numpy as np

from pypixxlib.propixx import PROPixxCTRL

# connect to VPixx device
try:
    device =  PROPixxCTRL()  
except:
    print("Could not connect to VPixx device. Make sure it is connected and powered on.")
    sys.exit(1)

# First, let's make a dictionary of codes that correspond to our buttons. This is in decimal.
# Note 1: these codes ARE NOT UNIVERSAL. You can check what your own button codes are using the PyPixx Digital I/O demo
# Note 2: these codes are for single button presses only. If two buttons are pressed at the same time this will generate a unique code, which we will ignore

# right hand button box of 2x5 setup / tested by dan, denis 2026-01-14
buttonCodes = {64768: 'blue', 64576: 'yellow', 64544: 'red',
               64640: 'green', 65024: 'white', 64512: 'button release'}
exitButton = 'white'

myLog = device.din.setDinLog(12e6, 1000)
device.din.startDinLog()
device.updateRegisterCache()
startTime = device.getTime()
finished = False

# let's create a loop which checks the schedule at 0.25 s intervals for button presses.
# Any time a button press is found, we print the timestamp and button pressed.
# If a designated exit button is pressed, we disconnect.

print("-- Press any of the buttons on the RIGHT 2x5 Button box setup")
print("   (white will quit!)")

core.wait(0.5) # give it 500ms to settle?

while finished == False:
    # read device status
    device.updateRegisterCache()
    device.din.getDinLogStatus(myLog)
    newEvents = myLog["newLogFrames"]

    if newEvents > 0:
        eventList = device.din.readDinLog(myLog, newEvents)

        for x in eventList:
            if x[1] in buttonCodes:
                # look up the name of the button
                buttonID = buttonCodes[x[1]]

                # get the time of the press, since we started logging
                time = round(x[0] - startTime, 2)
                printStr = 'Button pressed! Button code: ' + \
                    str(x[1]) + ', Button ID: ' + \
                    buttonID + ', Time:' + str(time)
                print(printStr)
                if buttonID == exitButton:
                    finished = True

# Stop logging
device.din.stopDinLog()
device.updateRegisterCache()
