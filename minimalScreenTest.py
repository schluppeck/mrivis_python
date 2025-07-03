#!/usr/bin/env python
# minimalScreenTest.py

# minimal screen test for PsychoPy
from psychopy import core, visual, event, gui, plugins
import numpy as np

# provide a compatibility layer for newer versions of PsychoPy
# and some site-specific parameters
import compatibility
from compatibility import waitForScanner


# create a window to draw in
# @TODO: fix this so optional params can be passed in

myWin = compatibility.createWindow()
myWin.mouseVisible = False

# hard coded params for this test
wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1, size=0.5,
                           visibleWedge=[0, 180], radialCycles=4,
                           angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0))  # this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1, size=0.5,
                           visibleWedge=[0, 180], radialCycles=4,
                           angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0))  # this stim changes too much for autologging to be useful

fixation = visual.PatchStim(myWin, tex=None, mask='circle', sf=0,
                            size=0.05,
                            name='fixation',
                            autoLog=False,
                            color=(1, 1, 0),
                            pos=(0, 0))


# from compatibility.py - reusable across code
t0, tdelta = waitForScanner(myWin)  # no fixation task passed in


clock = core.Clock()

# timing info for this loop?
# maybe should pass around global timer?
t = lastFPSupdate = 0
t_p = 0
trialClock = core.Clock()

expDuration = 10  # in seconds
flashPeriod = 0.5  # in seconds, so 2Hz


while trialClock.getTime() < expDuration:  # for 5 secs
    t = trialClock.getTime()
    t_diff = t-t_p
    # set stim type depending on where we are in the cycle
    if trialClock.getTime() < expDuration/2:
        if (t % flashPeriod) < (flashPeriod/2.0):  # (NB more accurate to use number of frames)
            stim = wedge1
        else:
            stim = wedge2
        stim.draw()

    else:
        pass
        # don't draw and let the win.flip() clear screen
    fixation.draw()
    myWin.flip()

    for key in event.getKeys():
        keyTime = trialClock.getTime()
        if key in ['escape', 'q']:
            print(myWin.fps())
            myWin.close()
            core.quit()
        elif key in [compatibility.PAUSE_KEY] and compatibility.ALLOW_PAUSE:
            # allow time for a screen shot, eg.
            core.wait(compatibility.PAUSE_TIME)

compatibility.endExperiment(myWin)

myWin.close()
core.quit()
