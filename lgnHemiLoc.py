#!/usr/bin/env python
# hemiLoc v2.1

# stimuli for visual hemifield localisation of LGN

# ./hemiLoc.py -h # for help
# ./hemiLoc.py -g # for entering values via GUI

from psychopy import core, visual, event, gui, plugins
import numpy as np

# provide a compatibility layer for newer versions of PsychoPy
# and some site-specific parameters
import compatibility

parser = compatibility.setupParser()
parser.add_argument('-bl', '--blockLength', default=12, type=float,
                    help='How long is the block on? (seconds)')
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
Visual stimulus that alternates a hemifield stimulus between left and right
'''

parser.epilog = './hemiLoc.py -bl 12 -nb 10 -np 0 -ss 1.0 -fp 0.25\n'
args = parser.parse_args()

# create a dictionary of parameters that can be passed to the GUI function
params = args.__dict__.copy()

tip = {
    'blockLength': 'length of on/off cycle',
    'numBlocks': 'number of blocks to run for',
    'nullPeriod': 'initial rest period',
    'stimSize': 'size of the stimulus in proportion to screen height',
    'flashPeriod': 'flash period (on/off cycle) in s',
}
params['timeStr'] = compatibility.getTimeStr()

if params['useGUI']:
    # if the user wants to use the GUI, create a dialog box
    dlg = gui.DlgFromDict(
        dictionary=params,
        title="Hemifield Localizer",
        fixed=['timeStr'],
        sortKeys=True,
        tip=tip)

    if not (dlg.OK):
        core.quit()  # user cancelled. quit

blockLength = params['blockLength']
numBlocks = params['numBlocks']
nullPeriod = params['nullPeriod']
stimSize = params['stimSize']
flashPeriod = params['flashPeriod']

# create a window to draw in
# @TODO: fix this so optional params can be passed in
#
myWin = compatibility.createWindow()
myWin.mouseVisible = False
# myWin.viewScale = [-1, -1]  # does this work now?

fixLength = 1.0/2
my_colors = {'red': [1, 0, 0],
             'green': [0, 1, 0],
             'blue': [0, 0, 1],
             'yellow': [1, 1, 0]}

rgb = np.array([1., 1., 1.])
two_pi = 2*np.pi

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

central_grey = visual.PatchStim(myWin, tex=None, mask='circle',
                                color=0*rgb,
                                size=.2*3)

merdianSpare = 10  # degrees to stay away from meridians

fixation = visual.PatchStim(myWin, tex=None, mask='circle', color=1*rgb,
                            size=1, units='deg')

wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1, size=stimSize,
                           visibleWedge=[0+merdianSpare, 181-merdianSpare], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0))  # this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1, size=stimSize,
                           visibleWedge=[0+merdianSpare, 181-merdianSpare], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False, ori=0, pos=(0, 0))  # this stim changes too much for autologging to be useful

wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=1, size=stimSize,
                           visibleWedge=[0+merdianSpare, 181-merdianSpare], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False, ori=180, pos=(0, 0))  # this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1, size=stimSize,
                           visibleWedge=[0+merdianSpare, 181-merdianSpare], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False, ori=180, pos=(0, 0))  # this stim changes too much for autologging to be useful

# if stepping through progressive values?
# initialOri = 0


compatibility.waitForScanner(myWin, fixation)


clock = core.Clock()

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

nTargs, nTargsH, nTargsC, nTargsF = 0, 0, 0, 0

targFlag = 0
targTime = 1000

# timing info for this loop?
# maybe should pass around global timer?

t = lastFPSupdate = 0
t_p = 0

for i in range(0, numBlocks):
    trialClock.reset()
    t_p = 0
    while trialClock.getTime() < blockLength:  # for 5 secs
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

        if trialClock.getTime() < blockLength/2:
            if (t % flashPeriod) < (flashPeriod/2.0):  # (NB more accurate to use number of frames)
                stim = wedge1
            else:
                stim = wedge2
        else:
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
            elif key in [compatibility.PAUSE_KEY] and compatibility.ALLOW_PAUSE:
                # allow time for a screen shot, eg.
                core.wait(compatibility.PAUSE_TIME)


nTargsC = max(nTargsC, 0)
print("nTargs:", int(nTargs))
print("nTargsH:", int(nTargsH))
print("nTargsF:", int(nTargsF))
print("nTargsC:", int(nTargsC))

print("Score: %.2f" % (nTargsC/nTargs*100))

compatibility.endExperiment(myWin)

myWin.close()
core.quit()
