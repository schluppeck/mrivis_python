#! /usr/bin/env python
# # minimalScreenTest.py

# minimal screen test for PsychoPy
import sys
import numpy as np
import argparse
from psychopy import core, visual, event, gui, plugins

# provide a compatibility layer for newer versions of PsychoPy
# the compatibility.py file is one folder up, so add to python path first!
# keep #noqa comments to avoid linter reordering import
sys.path.append('..')  # noqa
from compatibility import waitForScanner  # noqa
import compatibility  # noqa

# and some site-specific parameters
params = compatibility.setDefaultParams()

parser = compatibility.setupParser(
    'Minimal working screen example with some VPIXX triggering...')

# here is the place to add any specific arguments for this script
# w. parser.add_argument('--myparam', type=int, default=42, help='my param help')

# get the arguments out of this parser
args = parser.parse_args().__dict__.copy()

# reconcile default params and passed in / GUI specced arguments:
params = compatibility.reconcileParamsAndArgs(params, args)

# now import the VPIXX library if available
compatibility.loadVPixxLib(params)

# get a "device" for use in triggering
device = compatibility.getVPixxDevice(params)

# create a window to draw in

myWin = compatibility.createWindow(params=params)
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

# can also have a fixation task...

# from compatibility.py - reusable across code
# no fixation task passed in
t0, tdelta = waitForScanner(
    myWin,
    fixation=fixation,
    params=params,
    device=device)


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

    compatibility.checkForKeyTriggerOrQuit(myWin, params)

compatibility.endExperiment(myWin)

myWin.close()
core.quit()
