#!/usr/bin/env python
# oriMap v2.1

# stimuli for Ori column localisation, as copied from Yacoub et al 2008
# input arguments:

# 1 - blockLength - How long each 180 rotation lasts for
# 2 - numBlocks - How many cycles to run for
# 3 - nullPeriod - how long the blank period at the beginning of the session should run for
# 4 - stimSize - size of the stimulus in proportion to screen height
# 5 - initDir - rotation direction

# ./oriMap.py -h  # for help
# ./oriMap.py -g  # for entering values via GUI


from psychopy import core, visual, event, gui, plugins
from numpy import sin, pi
import math
import sys
import time
import numpy as np
import compatibility

from compatibility import waitForScanner

parser = compatibility.setupParser()
parser.add_argument('-bl', '--blockLength', default=60, type=float,
                    help='How long is the block? (seconds)')
parser.add_argument('-nb', '--numBlocks', default=10, type=int,
                    help='How many blocks?')
parser.add_argument('-np', '--nullPeriod', default=3,  type=float,
                    help='Duration of gray screen at start (seconds)')
parser.add_argument('-id', '--initDir', default=1, type=float,
                    help='Initial direction of rotation (1=clockwise, -1=counter-clockwise)')
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
Visual stimulus that goes through different orientations of grating stimuli to localise
orientation columns in the visual cortex
'''
parser.epilog = './oriMap.py --blockLength 60 --numBlocks 1 --nullPeriod 0 '

args = parser.parse_args()

# params = {
#     'blockLength': blockLength,
#     'numBlocks': numBlocks,
#     'nullPeriod': nullPeriod,
#     'stimSize': stimSize,
#     'initDir': initDir
# }
# params['timeStr'] = time.strftime("%b_%d_%H%M", time.localtime())
params = args.__dict__.copy()

if args.useGUI:
    dlg = gui.DlgFromDict(
        dictionary=params,
        title="Ori map localizer",
        fixed=['timeStr'])
    if not dlg.OK:
        core.quit()  # user cancelled. quit

blockLength = params['blockLength']
numBlocks = params['numBlocks']
nullPeriod = params['nullPeriod']
stimSize = params['stimSize']
flashPeriod = params['flashPeriod']
initDir = params['initDir']


# report the timing!
compatibility.reportTiming(params)

# @TODO: fix this so optional params can be passed in
#
myWin = compatibility.createWindow()
myWin.mouseVisible = False


rgb = np.array([1., 1., 1.])
two_pi = 2*np.pi

rotationRate = (1.0/blockLength)  # revs per sec

fixation = visual.ShapeStim(myWin,
                            lineColor='white',
                            lineWidth=2.0,
                            vertices=((-0.5, 0), (0.5, 0), (0, 0),
                                      (0, 0.5), (0, -0.5)),
                            interpolate=False,
                            closeShape=False,
                            pos=(0, 0))

fixation = visual.PatchStim(myWin, tex=None, mask='circle', sf=0, size=.2,
                            name='fixation', autoLog=False, color=(-1, -1, -1), pos=(0, 0))

central_grey = visual.PatchStim(myWin, tex=None, mask='raisedCos',
                                color=0*rgb, size=1*3)

fixation = visual.PatchStim(myWin, tex=None, mask='circle', color=1*rgb,
                            size=.4)

# INITIALISE SOME STIMULI
grating1 = visual.GratingStim(myWin, tex="sin", mask="raisedCos", texRes=256,
                              color=[1.0, 1.0, 1.0], colorSpace='rgb', opacity=1.0,
                              size=(18, 18), sf=(1.0, 1.0),
                              ori=0, depth=0.5, phase=0,
                              autoLog=False)  # this stim changes too much for autologging to be useful

initialOri = 0
compatibility.waitForScanner(myWin, fixation)

clock = core.Clock()

nullOri = initialOri-(initDir*rotationRate*nullPeriod*180)
grating1.setOri(nullOri)

color_key = 'white'
fn = 0
trialClock = core.Clock()

t = lastFPSupdate = 0
t_p = 0

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


# nTargs = 0
# nTargsH = 0
# nTargsC = 0
# nTargsF = 0
# targTime = 1000
# respFlag = 0

while trialClock.getTime() < nullPeriod:  # for 5 secs
    t = trialClock.getTime()
    t_diff = t-t_p

    fn = fixationInfo['fn']
    color_key = fixationInfo['color_key']
    my_colors = fixationInfo['my_colors']
    nTargs, nTargsH, nTargsC, nTargsF = 0, 0, 0, 0

    if t_diff > fixationInfo['fixLength']:
        old_color_key = color_key
        fnPrev = fn
        respFlag = 0
        while color_key == old_color_key:
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn > 2:
            respFlag = 1
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
        t_p = t

    grating1.setOri(nullOri+(t*initDir*rotationRate*180))
    if (t % 2 < 1):
        grating1.setPhase(t*4)
    else:
        grating1.setPhase(t*-4)

    fixation.draw()
    myWin.flip()

    for key in event.getKeys():
        keyTime = trialClock.getTime()
        if key in ['escape', 'q']:
            myWin.close()
            core.quit()
        elif key in ['1', '2', '3', '4']:
            if (keyTime-targTime) < 1:
                if respFlag:
                    nTargsC = nTargsC+1
                    nTargsH = nTargsH+1
                    respFlag = 0
            elif (keyTime-targTime) > 1:
                nTargsC = nTargsC-1
                nTargsF = nTargsF+1

t = lastFPSupdate = 0
t_p = 0

for i in range(0, (numBlocks)):
    trialClock.reset()
    t_p = 0
    my_colors = fixationInfo['my_colors']
    nTargs, nTargsH, nTargsC, nTargsF = 0, 0, 0, 0
    fn = fixationInfo['fn']
    while trialClock.getTime() < blockLength:  # for 5 secs
        t = trialClock.getTime()
        t_diff = t-t_p
        if t_diff > fixationInfo['fixLength']:
            old_color_key = color_key
            fnPrev = fn
            respFlag = 0
            while color_key == old_color_key:
                fn = np.random.randint(len(my_colors.keys()))
                color_key = list(my_colors.keys())[fn]
            this_color = my_colors[color_key]
            fixation.setColor(this_color)
            if fn > 2:
                respFlag = 1
                nTargs = nTargs + 1
                targTime = trialClock.getTime()
            t_p = t

        grating1.setOri(initialOri+(t*initDir*rotationRate*180))
        if (t % 2 < 1):
            grating1.setPhase(t*4)
        else:
            grating1.setPhase(t*-4)
        grating1.draw()
        central_grey.draw()
        fixation.draw()

        myWin.flip()

        for key in event.getKeys():
            keyTime = trialClock.getTime()
            if key in ['escape', 'q']:
                myWin.close()
                core.quit()
            elif key in ['1', '2', '3', '4']:
                if (keyTime-targTime) < 1:
                    if respFlag:
                        nTargsC = nTargsC+1
                        nTargsH = nTargsH+1
                        respFlag = 0
                elif (keyTime-targTime) > 1:
                    nTargsC = nTargsC-1
                    nTargsF = nTargsF+1

trialClock.reset()
t_p = 0
while trialClock.getTime() < nullPeriod:  # for 5 secs
    t = trialClock.getTime()
    t_diff = t-t_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        respFlag = 0
        while color_key == old_color_key:
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn > 2:
            respFlag = 1
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
        t_p = t

    grating1.setOri(nullOri+(t*initDir*rotationRate*180))
    if (t % 2 < 1):
        grating1.setPhase(t*4)
    else:
        grating1.setPhase(t*-4)
    # grating1.draw()
    fixation.draw()

    myWin.flip()

    for key in event.getKeys():
        keyTime = trialClock.getTime()
        if key in ['escape', 'q']:
            myWin.close()
            core.quit()
        else:
            if (keyTime-targTime) < 1:
                if respFlag:
                    nTargsC = nTargsC+1
                    nTargsH = nTargsH+1
                    respFlag = 0
            elif (keyTime-targTime) > 1:
                nTargsC = nTargsC-1
                nTargsF = nTargsF+1

nTargsC = max(nTargsC, 0)
print("nTargs:", int(nTargs))
print("nTargsH:", int(nTargsH))
print("nTargsF:", int(nTargsF))
print("nTargsC:", int(nTargsC))

print("Score: %.2f" % (nTargsC/nTargs*100))

myWin.close()
core.quit()
