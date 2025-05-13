# compatibility layer
# making sure we have a consistent interface across
# all different scripts in this folder.
#
# this can also contain some site-specific parameters.
#
# 2025-05-05, ds

import psychopy
from psychopy import core, visual, event, gui, plugins
import sys
import argparse
import time
import numpy as np

# default parameters
SCREEN_SIZE = (1920, 1080)
CHECK_TIMING = False
# allow
ALLOW_PAUSE = True
PAUSE_KEY = 'p'
PAUSE_TIME = 10  # seconds for e.g screen caputre


def versionCheck():
    """
    Check the version of psychopy and return True if it's modern (>= 2020.1.0)
    """
    version = psychopy.__version__
    if str(version) < '2020.1.0':
        print("(compatibility) running an older version of psychopy")
        return False
    else:
        print(f"\n(compatibility) modern version of psychopy. v{version}")
        psychopy_modern = True
        plugins.activatePlugins()  # needed for modern version
        # PatchStim migrated to GratingStim in newer version
        visual.PatchStim = visual.GratingStim
        return True


def setupParser():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0])
    return parser


def createWindow():
    """
    Create a window for the experiment.
    """
    myWin = visual.Window(SCREEN_SIZE,
                          allowGUI=False,
                          bitsMode=None,
                          units='height',
                          fullscr=1,
                          winType='pyglet',
                          monitor='testMonitor',
                          checkTiming=CHECK_TIMING,
                          color=0)
    return myWin


def reportTiming(params):
    """
    Report the timing of the experiment.
    """
    onLength = params['onLength']
    offLength = params['offLength']
    numBlocks = params['numBlocks']
    nullPeriod = params['nullPeriod']
    stimSize = params['stimSize']
    flashPeriod = params['flashPeriod']

    print(f"on/off: {onLength}/{offLength}")
    print(f"numBlocks: {numBlocks}")
    print(f"nullPeriod: {nullPeriod}")
    totalTime = (onLength + offLength) * numBlocks + nullPeriod
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


def showNullPeriod(myWin, fixation, fixationInfo, nullPeriod):
    """
    Show the null period before the experiment starts.
    """
    # loop
    t = lastFPSupdate = 0
    t_p = 0
    trialClock = core.Clock()

    # get a local color_key
    color_key = fixationInfo['color_key']
    fn = fixationInfo['fn']
    my_colors = fixationInfo['my_colors']
    fixLength = fixationInfo['fixLength']
    nTargs, nTargsH, nTargsC, nTargsF = 0, 0, 0, 0

    while trialClock.getTime() < nullPeriod:
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
            if fn > 2:
                nTargs = nTargs + 1
                targTime = trialClock.getTime()
                targFlag = 1
            t_p = t

        fixation.draw()

        myWin.flip()

        for key in event.getKeys():
            keyTime = trialClock.getTime()
            if key in ['escape', 'q']:
                print(myWin.fps())
                myWin.close()
                core.quit()
            elif key in ['1', '2', '3', '4']:
                if targFlag:
                    if (keyTime-targTime) < 1:
                        nTargsC = nTargsC+1
                        nTargsH = nTargsH+1
                        targFlag = 0
                else:
                    nTargsC = nTargsC-1
                    nTargsF = nTargsF+1

    # store away C, H
    fixationInfo['nTargs'] += nTargs
    fixationInfo['nTargsH'] += nTargsH
    fixationInfo['nTargsC'] += nTargsC
    fixationInfo['nTargsF'] += nTargsF

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
