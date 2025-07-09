# this is code from Michael that works.
# tested on the windows side, but now also to be used on the linu


from pypixxlib.propixx import PROPixxCTRL  #if you have a datapixx3 change this to “from pypixxlib.datapixx import DATAPixx3”
from psychopy import core
#import keyboard

#connect to VPixx device
device = PROPixxCTRL()   #if you have a datapixx3 change this to “device = DATAPixx3”

myLog = device.din.setDinLog(12e6, 1000)
device.din.startDinLog()
device.updateRegisterCache()
startTime = device.getTime()

#let's create a loop which checks the schedule for triggers.
#Any time a trigger is detected, we print the timestamp and DIN state.

print('(checkDIO) waiting for scanner')

while True:
    #read device status
    device.updateRegisterCache()
    device.din.getDinLogStatus(myLog)
    newEvents = myLog["newLogFrames"]

    # if keyboard.is_pressed('q'):
    #     print("Exiting.")
    #     break

    if newEvents > 0:
        eventList = device.din.readDinLog(myLog, newEvents)

        for x in eventList:
            print(x)
        break
    
#Stop logging
device.din.stopDinLog()
device.updateRegisterCache()



# import pypixxlib.datapixx as dp
# # DATAPixx2() working by ds's testing. 2025

# my_device = dp,DATAPixx()
# din_state = my_device.din.getValue()

# # Start your experiment
# experiement_is_running = True

# while experiement_is_running:
#     old_state = din_state
#     my_device.updateRegisterCache()
#     din_state = my_device.din.getValue()

#     if old_state is not din_state: # Something triggered.
#         # Now we want to check, for example, if pin 6 triggered.
#         if (old_state & 2**6) is not (din_state & 2**6):
#             print('Pin 6 triggered!')
#             experiement_is_running = False

#         else:
#             print('Pin 6 is in the same state as before')

# # Finish your experiment

# print("checked DIGITAL IN...")