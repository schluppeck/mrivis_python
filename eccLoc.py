#!/usr/bin/env python
# eccLoc v1.1

# stimuli for visual field localisation (eccentricity)

# ./eccLoc.py -h  # for help
# ./eccLoc.py -g  # for entering values via GUI


# input arguments:
# 1 - onLength - How long block is on
# 2 - numBlocks - How many blocks of hemifield stimulation to run for (must be even for equal number of R and L)
# 3 - nullPeriod - how long the blank period at the beginning of the session should run for
# 4 - stimSize - size of the stimulus in proportion to screen height


import psychopy
from psychopy import core, visual, event, gui, plugins
from numpy import sin, pi
import math
import sys
import time
import numpy as np

# provide a compatibility layer for newer versions of PsychoPy
# and some site-specific parameters
import compatibility
from compatibility import waitForScanner

parser = compatibility.setupParser()
parser.add_argument('-on', '--onLength', default=12, type=float,
                    help='How long is the block on? (seconds)')
parser.add_argument('-off', '--offLength', default=12, type=float,
                    help='How long is the block off? (seconds)')
parser.add_argument('-nb', '--numBlocks', default=10, type=int,
                    help='How many blocks?')
parser.add_argument('-np', '--nullPeriod', default=10,  type=float,
                    help='Duration of gray screen at start (seconds)')
parser.add_argument('-ss', '--stimSize', default=1.0, type=float,
                    help='Stimulus size (fraction of screen height)')
parser.add_argument('-fp', '--flashPeriod', default=0.25, type=float,
                    help='Flash period (seconds)')
parser.add_argument('-g', help='Use the GUI to set params',
                    dest='useGUI', action='store_true')
parser.add_argument('-v', help='Set verbose output',
                    dest='verbose', action='store_true')

# specific help for this program
parser.description = '''
Visual stimulus that alternates a ring of given eccentricity A
with an off block, the eccentricity B with off block.

The eccentricity (full height) corresponds to 1.0 (default),
and A and B annuli together cover the full extent of that range
'''

parser.epilog = './eccLoc.py --onLength 12 --offLength 0 --numBlocks 1 --nullPeriod 0 '

args = parser.parse_args()

# create a dictionary of parameters that can be passed to the GUI function
params = args.__dict__.copy()

tip = {
    'onLength': 'length of on blocks',
    'offLength': 'length of off blocks',
    'numBlocks': 'number of blocks (centre on/off/surround on/off) to run for',
    'nullPeriod': 'initial rest period',
    'stimSize': 'size of the stimulus in proportion to screen height',
    'flashPeriod': 'flash period (on/off or +1/-1 cycle) in s',
}
params['timeStr'] = compatibility.getTimeStr()

# if GUI is asked for show it
if args.useGUI:
    dlg = gui.DlgFromDict(
        dictionary=params,
        title="Eccentricity Localizer",
        fixed=['timeStr'],
        sortKeys=True,
        tip=tip)

    if dlg.OK:
        pass  # print(params)
    else:
        core.quit()  # user cancelled. quit
else:
    pass  # print(params)

# repackage into individual variables that will be used below
onLength = params['onLength']
offLength = params['offLength']
numBlocks = params['numBlocks']
nullPeriod = params['nullPeriod']
stimSize = params['stimSize']
flashPeriod = params['flashPeriod']

# report the timing!
compatibility.reportTiming(params)

# create a window to draw in
# @TODO: break this out to compatibility.py
myWin = visual.Window(compatibility.SCREEN_SIZE,
                      allowGUI=False,
                      bitsMode=None,
                      units='height',
                      fullscr=1,
                      winType='pyglet',
                      monitor='testMonitor',
                      checkTiming=compatibility.CHECK_TIMING,
                      color=0)
myWin.mouseVisible = False


rgb = np.array([1., 1., 1.])
two_pi = 2*np.pi

rotationRate = (1.0 / onLength)  # revs per sec

# @TODO: break this out to compatibility.py
# these fixations are overwritten later. Keep the one we want
fixation = visual.ShapeStim(myWin,
                            lineColor='white',
                            lineWidth=2.0,
                            vertices=((-0.5, 0), (0.5, 0), (0, 0),
                                      (0, 0.5), (0, -0.5)),
                            interpolate=False,
                            closeShape=False,
                            pos=(0, 0))

fixation = visual.PatchStim(myWin, tex=None, mask='circle', sf=0, size=.1,
                            name='fixation', autoLog=False, color=(-1, -1, -1), pos=(0, 0))

central_grey = visual.PatchStim(myWin, tex=None, mask='circle',
                                color=0*rgb,
                                size=.2*3)

fixation = visual.PatchStim(myWin, tex=None, mask='circle', color=1*rgb,
                            size=.01)  # ,units='deg')

oneCycle = np.arange(0, 1.0, 1/128.0)
oneCycle = np.where(oneCycle < (64/128), 1, 0)
thisStart = 0+0*(64/128)
theseIndices = np.arange(thisStart, thisStart+1, 1/128.0) % 1.0
theseIndices = (theseIndices*128).astype(np.uint8)
thisMask = oneCycle[theseIndices]

wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1, size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0))  # this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1, size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0))  # this stim changes too much for autologging to be useful

oneCycle = np.arange(0, 1.0, 1/128.0)
oneCycle = np.where(oneCycle <= (64/128), 1, 0)
thisStart = 0+1*(64/128)
theseIndices = np.arange(thisStart, thisStart+1, 1/128.0) % 1.0
theseIndices = (theseIndices*128).astype(np.uint8)
thisMask = oneCycle[theseIndices]

wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=1, size=stimSize,
                           visibleWedge=[0, 360], radialCycles=8, angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0), mask=thisMask)  # this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1, size=stimSize,
                           visibleWedge=[0, 360], radialCycles=8, angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0), mask=thisMask)  # this stim changes too much for autologging to be useful

# from compatibility.py - reusable across code
t0, tdelta = waitForScanner(myWin, fixation)

if params['verbose']:
    print(f"t0, tdelta: {t0},  {tdelta}")

clock = core.Clock()


# dict that keeps info related to hits, etc on fixation targets
# should go into a funciont
fixationInfo = {
    'nTargsH': 0,
    'nTargs': 0,
    'nTargsC': 0,
    'nTargsF': 0,
    'targTime': 1000,
    'targFlag': 0,
    'color_key': 'white',
    'fn': 0,
    'my_colors': {'red': [1, 0, 0],
                  'green': [0, 1, 0],
                  'blue': [0, 0, 1],
                  'yellow': [1, 1, 0]},
    'fixLength': 1.0/2
}

fixationInfo = compatibility.showNullPeriod(
    myWin, fixation, fixationInfo, nullPeriod)
# show the fixation cross for the null period

# timing info for this loop?
# maybe should pass around global timer?
t = lastFPSupdate = 0
t_p = 0
trialClock = core.Clock()


for i in range(0, (numBlocks)):
    trialClock.reset()
    t_p = 0
    fn = fixationInfo['fn']
    color_key = fixationInfo['color_key']
    my_colors = fixationInfo['my_colors']
    nTargs, nTargsH, nTargsC, nTargsF = 0, 0, 0, 0
    while trialClock.getTime() < (2*(onLength+offLength)):  # for 5 secs
        t = trialClock.getTime()
        t_diff = t-t_p
        if t_diff > fixationInfo['fixLength']:
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
        # set stim type depending on where we are in the cycle
        if trialClock.getTime() < onLength:
            if (t % flashPeriod) < (flashPeriod/2.0):  # (NB more accurate to use number of frames)
                stim = wedge1
            else:
                stim = wedge2
            stim.draw()
        elif trialClock.getTime() < ((2*onLength)+offLength) and trialClock.getTime() > (onLength+offLength):
            if (t % flashPeriod) < (flashPeriod/2.0):  # (NB more accurate to use number of frames)
                stim = wedge3
            else:
                stim = wedge4
            stim.draw()

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

nTargsC = max(nTargsC, 0)
print("nTargs:", int(nTargs))
print("nTargsH:", int(nTargsH))
print("nTargsF:", int(nTargsF))
print("nTargsC:", int(nTargsC))

print("Score: %.2f" % (nTargsC/nTargs*100))

compatibility.endExperiment(myWin)

myWin.close()
core.quit()
