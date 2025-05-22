# compatibility layer
# making sure we have a consistent interface across
# all different scripts in this folder.
#
# this can also contain some site-specific parameters.
#
# 2025-05-05, ds

# import psychopy
from psychopy import core, visual, event, plugins
from psychopy import __version__ as PSYCHOPY_VERSION
import sys
import argparse
import time
import numpy as np


# connect to VPixx device
USE_VPIXX = False

# default parameters
CODING_WINDOW = True  # if true, make a small, non-fullscreen window for coding
SCREEN_SIZE = np.array([1920, 1080])  # size of the screen
CHECK_TIMING = False

# FIXATION stuff, set defaults here.
FIXATION_INFO = {
    'nTargsH': 0,
    'nTargs': 0,
    'nTargsC': 0,
    'nTargsF': 0,
    'targTime': 1000,
    'targFlag': 0,
    'color_key': 'white',
    'fn': 0,
    'targetType': 'circle',  # or 'circle'
    'fixationSize': 0.05,
    'fixationLineWidth': 8.0,
    'my_colors': {'red': [1, 0, 0],
                  'green': [0, 1, 0],
                  'blue': [0, 0, 1],
                  'yellow': [1, 1, 0]},  # target color
    'fixLength': 1.0 / 2
}

BUTTON_CODES = ['1', '2', '3', '4']  # keyboard. fix for VPIXX.

# allow interruptions for screen capture
ALLOW_PAUSE = True
PAUSE_KEY = 'p'
PAUSE_TIME = 10  # seconds for e.g screen caputre

if USE_VPIXX:
    try:
        import pypixxlib
        print("(compatibility) using pypixxlib")
    except ImportError:
        print("(compatibility) pypixxlib not found. Need this for triggers. etc")
        pypixxlib = None
        print("Exiting... for now - need to fix this to use buttons?")
        core.quit()


def versionCheck():
    """
    Check the version of psychopy and return True if it's modern (>= 2020.1.0)
    """
    if str(PSYCHOPY_VERSION) < '2020.1.0':
        print("(compatibility) running an older version of psychopy")
        return False
    else:
        print(
            f"\n(compatibility) modern version of psychopy. version: {PSYCHOPY_VERSION}")
        psychopy_modern = True
        plugins.activatePlugins()  # needed for modern version
        # PatchStim migrated to GratingStim in newer version
        visual.PatchStim = visual.GratingStim
        return True


def setupParser():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0])
    return parser


def createWindow(units='height'):
    """
    Create a window for the experiment.
    """
    # create window, taking into account debug choices
    screenSize = SCREEN_SIZE/2 if CODING_WINDOW else SCREEN_SIZE
    fullscr = False if CODING_WINDOW else True
    allowGUI = True if CODING_WINDOW else False
    pos = (50, 50) if CODING_WINDOW else None
    myWin = visual.Window(screenSize,
                          allowGUI=allowGUI,
                          bitsMode=None,
                          checkTiming=CHECK_TIMING,
                          color=0,
                          fullscr=fullscr,
                          monitor='testMonitor',
                          pos=pos,
                          units=units,
                          winType='pyglet')
    return myWin


def createFixation(myWin, fixationInfo=None):
    """
    Create a fixation target for the experiment.
    """
    # create fixation / using defaults if not passed in!
    fixationInfo = FIXATION_INFO if fixationInfo is None else fixationInfo
    fixationLineWidth = fixationInfo['fixationLineWidth']
    fixationSize = fixationInfo['fixationSize']
    if fixationInfo['targetType'] == 'circle':
        fixation = visual.PatchStim(myWin, tex=None, mask='circle', sf=0,
                                    size=fixationSize,
                                    name='fixation', autoLog=False, color=(-1, -1, -1), pos=(0, 0))

    elif fixationInfo['targetType'] in ["cross", "line"]:
        fixation = visual.ShapeStim(myWin, lineColor='white',
                                    lineWidth=fixationLineWidth,
                                    vertices=((-fixationSize, 0), (fixationSize, 0),
                                              (0, 0), (0, fixationSize), (0, -fixatoinSize)),
                                    interpolate=False,
                                    closeShape=False,
                                    pos=(0, 0))

    return fixation


def reportTiming(params):
    """
    Report the timing of the experiment.
    """
    # onLength = params['onLength']
    # offLength = params['offLength']
    # numBlocks = params['numBlocks']
    # nullPeriod = params['nullPeriod']
    # stimSize = params['stimSize']
    # flashPeriod = params['flashPeriod']

    # print(f"on/off: {onLength}/{offLength}")
    # print(f"numBlocks: {numBlocks}")
    # print(f"nullPeriod: {nullPeriod}")
    # totalTime = (onLength + offLength) * numBlocks + nullPeriod
    for (key, value) in params.items():
        print(f"{key}: {value}")

    totalTime = "BLA - to be fixed"
    print(f"-----------------------------------")
    print(f"TOTAL (s): {totalTime}")


def waitForScanner(myWin, fixation):
    """
    Wait for the scanner to start.
    """
    # @TODO make sure it works with VPIXX trigger (not 5!)
    # create text stimuli
    message1 = visual.TextStim(myWin, pos=[
                               0, +.5], wrapWidth=1.5, color='#000000', alignText='center', name='topMsg', text="aaa", units='norm')
    message2 = visual.TextStim(myWin, pos=[0, -.5], wrapWidth=1.5, color='#000000',
                               alignText='center', name='bottomMsg', text="bbb", units='norm')

    # wait for scanner
    message1.setText("Please fixate on the central dot during the visual task")
    message2.setText("Press a button when you see a yellow dot at fixation")
    message1.draw()
    message2.draw()
    myWin.flip()
    event.waitKeys()

    kwait = 1
    t0 = core.getTime()
    while kwait:
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['5', 't']:
                kwait = 0
                t1 = core.getTime()
            elif key in ['escape', 'q']:
                print(myWin.fps())
                myWin.close()
                core.quit()
    return t1, t1-t0


def fixationTask(myWin, fixationInfo, targTime=None, targFlag=None, trialClock=None):
    """
    Function that checks keyboard presses, etc.
    Encapulates the task of checking for key presses and updating the fixation information.
    """
    # set locally
    nTargsH, nTargsC, nTargsF = 0, 0, 0
    # loop through all keys
    for key in event.getKeys():
        keyTime = trialClock.getTime()
        if key in ['escape', 'q']:
            print(myWin.fps())
            myWin.close()
            core.quit()
        elif key in BUTTON_CODES:
            if targFlag:
                # if there was a target and a response
                # HIT
                if (keyTime-targTime) < 1:  # if within 1s
                    nTargsC = nTargsC+1
                    nTargsH = nTargsH+1
                    targFlag = 0
            else:
                # if there was no target but a response
                # FALSE ALARM
                nTargsC = nTargsC-1
                nTargsF = nTargsF+1

    # store away C, H
    # fixationInfo['nTargs'] += nTargs
    fixationInfo['nTargsH'] += nTargsH
    fixationInfo['nTargsC'] += nTargsC
    fixationInfo['nTargsF'] += nTargsF

    return fixationInfo


def pickFixationColor(fixationInfo, trialClock=None, t_p=None):
    # get a local color_key
    color_key = fixationInfo['color_key']
    fn = fixationInfo['fn']
    my_colors = fixationInfo['my_colors']
    fixLength = fixationInfo['fixLength']
    nTargs = 0
    targFlag = 0
    targTime = 0

    # get the time
    t = trialClock.getTime()
    t_diff = t-t_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        while color_key == old_color_key:
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn == 3:  # target
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
            targFlag = 1

        t_p = t  # reset the time

    return targTime, targFlag


def showNullPeriod(myWin, fixation, fixationInfo, nullPeriod):
    """
    Show the null period before the experiment starts.
    """
    # loop
    # t = lastFPSupdate = 0
    t_p = 0
    trialClock = core.Clock()

    targFlag = 0
    targTime = 0

    # for the duration of the null period
    while trialClock.getTime() < nullPeriod:

        targTime, targFlag = pickFixationColor(fixationInfo, trialClock, t_p)

        fixation.draw()

        myWin.flip()

        # function that checks keyboard presses, etc.
        fixationInfo = fixationTask(
            myWin, fixationInfo, targTime, targFlag, trialClock)

    return fixationInfo


def endExperiment(myWin):
    """
    End the experiment and show a thank you message.
    """
    # create text stimuli
    message1 = visual.TextStim(myWin, pos=[
                               0, +.5], wrapWidth=1.5, color='#000000', alignText='center', name='topMsg', text="aaa", units='norm')
    message2 = visual.TextStim(myWin, pos=[0, -.5], wrapWidth=1.5, color='#000000',
                               alignText='center', name='bottomMsg', text="bbb", units='norm')

    # show thank you message
    message1.setText("Thank you!")
    message2.setText("Press 'q' or 'escape' to end the session.")
    myWin.clearBuffer()  # clear the screen
    message1.draw()
    message2.draw()
    myWin.flip()
    thisKey = event.waitKeys(keyList=['q', 'escape'])


def getTimeStr():
    """
    Get the current time as a string.
    """
    return time.strftime("%Y-%m-%dT%H%M%S", time.localtime())

# this is a compatibility layer for the scripts in this folder.
# actually do the version check (if it's being imported)
# can add code in here that will be run if this module is being imported.
# setting defaults, etc.


if __name__ != "__main__":
    versionCheck()
    print("(compatibility) version check.")
else:
    print("(!!) This script is not meant to be run directly. It is a compatibility layer for other scripts.")
    sys.exit(1)
