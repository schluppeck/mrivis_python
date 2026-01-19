#!/usr/bin/env python

# stimuli for retinotopic mapping
# original code by jwp
# updated for PsychoPy3 by ab
# refactored for use on VPIXX at SPMIC by ds
# can measure vf centre and coverage usin visualField.py

from psychopy import visual, event, core, monitors, gui,  plugins  # misc
from psychopy import hardware
import numpy as np
import compatibility
from compatibility import waitForScanner, SlidingAnnulus, SlidingWedge

# last run of visual field
# try:
#     # try to load previous info
#     visField = misc.fromFile('visualFieldParams.pickle')
# except:
# if no file use some defaults
visField = {'centre_x': 0.,
            'centre_y': 0.,
            'size': 1.0}  # size of stimulus in heigh

# and some site-specific parameters
params = compatibility.setDefaultParams()

parser = compatibility.setupParser(
    'Minimal working screen example with some VPIXX triggering...')

# here is the place to add any specific arguments for this script

parser.add_argument('-obs', '--observer', default='sub01', type=str,
                    help='Observer code')
parser.add_argument('-dir', '--direction',
                    choices=['exp', 'con', 'cw', 'ccw'], default='ccw',
                    help='exp(anding) or con(tracting) rings, cw or ccw wedge')
parser.add_argument('-ct', '--cycleTime', default=24, type=float,
                    help='How long to complete one cycle (seconds)')
parser.add_argument('-nc', '--nCycles', default=5, type=int,
                    help='How many blocks?')
parser.add_argument('-np', '--nullPeriod', default=0.0,  type=float,
                    help='Duration of gray screen at start (seconds)')
parser.add_argument('-ss', '--stimSize', default=1.0, type=float,
                    help='Stimulus size (fraction of screen height)')
parser.add_argument('-dcw', '--dutyCycleWedge', default=0.125, type=float,
                    help='Duty cycle for wedge (fraction)')
parser.add_argument('-dcr', '--dutyCycleRing', default=0.25, type=float,
                    help='Duty cycle for ring (fraction)')
parser.add_argument('-ar', '--angularRate', default=0.3, type=float,
                    help='Angular rate of change')
parser.add_argument('-cp', '--changeProbability', default=0.05, type=float,
                    help='Probability of direction change (per frame)')
parser.add_argument('-fp', '--flashPeriod', default=0.25, type=float,
                    help='Flash period (seconds)')
parser.add_argument('-e', '--exportStimImage', help='Export stimulus (requires -tr)',
                    dest='exportStimImage', action='store_true')
parser.add_argument(
    '-tr', '--TR', help='TR / dynamic scan time (required for -e)',
    dest='TR', type=float, default=None)

# specific help for this program
parser.description = '''
Travelling wedge or annulus stimulus for retinotopic mapping

Exp, con, cw, ccw - as per e.g. matlab implementations of the same.
'''
parser.epilog = './retinotopy.py --onLength 12 --offLength 0 --numBlocks 1 --nullPeriod 0 '

# get the arguments out of this parser
args = parser.parse_args().__dict__.copy()

# reconcile default params and passed in / GUI specced arguments:
params = compatibility.reconcileParamsAndArgs(params, args)

# check here that if -e flag is set that TR is also set
if params['exportStimImage']:
    if args.TR is None or args.TR <= 0:
        parser.error('-e flag requires valid -tr [>= 0] argument')
        # automatically quits. export requires window so do that later.

params['timeStr'] = compatibility.getTimeStr()

# set some more that don't change
params['size'] = float(visField['size'])
params['centre_x'] = visField['centre_x']
params['centre_y'] = visField['centre_y']

# now import the VPIXX library if available
compatibility.loadVPixxLib(params)


print("Observer:%s, run:%s, time:%s" %
      (params['observer'], params['direction'], params['timeStr']))

if params['exportStimImage']:
    myWin = compatibility.createWindow(screenSize=(192/2, 108/2))
    # on the mac w/ retina displays: contentScaleFactor = 2!
    myWin.mouseVisible = True
else:
    myWin = compatibility.createWindow(params=params)  # use defaults
    myWin.mouseVisible = False

# deal with exporting only...
if params['exportStimImage']:
    print(f'Exporting stimulus images with TR=%.2f sec' % (params['TR']))
    # do the export and then finish.
    compatibility.exportStimulusImage(myWin, params, fileFormat='mat')
    exit(0)

# class definitions moved to compatibility.py!

# parameter that affect timing of wedge / annulus redrawing (sliding)

changeProbability = params['changeProbability']
angularRate = params['angularRate']

params['centre'] = np.array((params['centre_x'], params['centre_y']))

if params['direction'] in ['cw', 'ccw']:
    # create an instance of our wedge
    wedge = SlidingWedge(myWin, pos=params['centre'], size=params['size'],
                         dutyCycle=params['dutyCycleWedge'])  # changeProb=changeProbability, angularRate=angularRate
else:
    annulus = SlidingAnnulus(myWin, pos=params['centre'], size=params['size'],
                             dutyCycle=params['dutyCycleRing'],
                             changeProb=changeProbability, angularRate=angularRate)
    # annulus = FlickeringAnnulus(myWin, pos=params['centre'], size=params['size'],
    #                            dutyCycle=params['dutyCycleRing'])


# always need a fixation point
# fixation = visual.PatchStim(myWin, mask='circle', tex=None,
#                             size=0.1, pos=params['centre'])
fixationInfo = params['FIXATION_INFO']
fixation = compatibility.createFixation(myWin, fixationInfo=fixationInfo)


# get rotation speed in deg/sec
if params['direction'] == 'cw':
    cycleSpeed = 360.0/params['cycleTime']
elif params['direction'] == 'ccw':
    cycleSpeed = -360.0/params['cycleTime']
elif params['direction'] == 'exp':
    cycleSpeed = -1.0/params['cycleTime']
elif params['direction'] == 'con':
    cycleSpeed = 1.0/params['cycleTime']


def quit():
    print('user quit before end of run')
    myWin.close()
    core.quit()


# update and wait for the go signal
myWin.update()

# from compatibility.py - reusable across code
t0, tdelta = waitForScanner(myWin, fixation=fixation, params=params)

fixationInfo = compatibility.showNullPeriod(
    myWin, fixation, fixationInfo, params['nullPeriod'])

globalClock = core.Clock()
g = 0
lastSwitch = globalClock.getTime()

while g < params['cycleTime']*params['nCycles']:
    g = globalClock.getTime()

    if params['direction'] in ['cw', 'ccw']:
        wedge.incrementPhase()
        wedge.setOri(cycleSpeed*g)
        wedge.draw()

    elif params['direction'] in ['exp', 'con']:
        annulus.incrementRotation()
        annulus.setPhase((cycleSpeed*g) % 1)
        annulus.draw()

    fixation.draw()
    myWin.update()

    for key in event.getKeys():
        if key in ['escape', 'q']:
            quit()

print('%%%%%%%%%%%%%%%%%')
print("completed %s run. t=%.2f. meanFPS=%.1f" %
      (params['direction'], globalClock.getTime(), myWin.fps()))
print('%%%%%%%%%%%%%%%%%')

compatibility.endExperiment(myWin)
myWin.close()
core.quit()
