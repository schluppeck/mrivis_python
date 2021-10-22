#!/usr/bin/env python
# visualLoc v2.0

# stimuli for visual field localisation
# input arguments:
# 1 - blockLengthOn - How long each visual stimulus is on
# 2 - blockLengthOff - How long each visual stimulus is off
# 3 - numBlocks - How many blocks of on/off to run for
# 4 - nullPeriod - how long the off period at the beginning of the session should run for
# 5 - stimSize - size of the stimulus in proportion to screen height
# 6 - flashPeriod - length the one flash period

# parameters can be set using the input arguments above - if the stimulus goes off the edge of the screen, reduce stimSize, or increase if there's dead-space at the edge of the screen.'
# stimulus length = ([blockLength*numBlocks)+nullPeriod

# parameters can be set either via commnand line arguments or GUI
# if all arguments passed in, assume user is happy with parameters and GUI will not appear

from psychopy import core, visual, event, gui, data
from psychopy.tools.filetools import fromFile,toFile # saving and loading parameter files
from numpy import sin, pi
import math,sys,time
import numpy as np

if len(sys.argv)>1:
    blockLengthOn=float(sys.argv[1])
else:
    blockLengthOn=16
    
if len(sys.argv)>2:
    blockLengthOff=float(sys.argv[2])
else:
    blockLengthOff=blockLengthOn

if len(sys.argv)>3:
    numBlocks=int(sys.argv[3])
else:
    numBlocks=10

if len(sys.argv)>4:
    nullPeriod=float(sys.argv[4])
else:
    nullPeriod=blockLengthOff/2

if len(sys.argv)>5:
    stimSize=float(sys.argv[5])
else:
    stimSize=1.0
    
if len(sys.argv)>6:
    flashPeriod=float(sys.argv[6])
else:
    flashPeriod=0.25

params = {
        'blockLengthOn':blockLengthOn,
        'blockLengthOff':blockLengthOff,
        'numBlocks': numBlocks,
        'nullPeriod': nullPeriod,
        'stimSize': stimSize,
        'flashPeriod': flashPeriod,
        }
params['timeStr']= time.strftime("%b_%d_%H%M%S", time.localtime())

if len(sys.argv)<6:
    dlg = gui.DlgFromDict(
            dictionary=params,
            title="Visual Localizer",
            fixed=['timeStr'],
            sort_keys=False,
            order=['numBlocks','blockLengthOn','blockLengthOff','nullPeriod','stimSize','flashPeriod','timeStr'])

    if dlg.OK:
        print(params)
    else:
        core.quit() #user cancelled. quit
else:
    print(params)

# basic logfile - make a note of which parameters were run, and when the scan was run
with open("visualLoc" + params['timeStr'] + ".txt", 'w') as f: 
    for key, value in params.items(): 
        f.write('%s:%s\n' % (key, value))

blockLengthOn = params['blockLengthOn']
blockLengthOff = params['blockLengthOff']
numBlocks = params['numBlocks']
nullPeriod = params['nullPeriod']
stimSize = params['stimSize']
flashPeriod = params['flashPeriod']

#create a window to draw in
myWin =visual.Window((1280,800),allowGUI=False,
bitsMode=None, units='height', fullscr=0,winType='pyglet',monitor='testMonitor', color=0)

fixLength=1.0/2
my_colors = {'red':[1,0,0],
             'green':[0,1,0],
             'blue':[0,0,1],
             'yellow':[1,1,0]}

rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi

#rotationRate = (1.0/blockLength) #revs per sec
#flashPeriod = 0.25 

central_grey = visual.PatchStim(myWin, tex=None, mask='circle', 
                           color=0*rgb, size=.2*3)

fixation = visual.PatchStim(myWin, tex=None, mask = 'circle',color=1*rgb,
                                size=1, units='deg')

wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=stimSize,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=stimSize,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful

kwait = 1
while kwait:
    fixation.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['5']:
            kwait = 0
        elif key in ['escape','q']:
            print(myWin.fps())
            myWin.close()
            core.quit()

clock=core.Clock()

color_key = 'white'
fn = 0;
trialClock = core.Clock()

t = lastFPSupdate = 0
t_p = 0

nTargs = 0;
nTargsH = 0;
nTargsC = 0;
nTargsF = 0;
targTime= 1000;
targFlag=0;

while trialClock.getTime()<nullPeriod:#for 5 secs
    t=trialClock.getTime()
    t_diff=t-t_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        while color_key == old_color_key: 
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn>2:
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
            targFlag = 1
        t_p = t
    fixation.draw()
    myWin.flip()
    for key in event.getKeys():
        keyTime=trialClock.getTime()
        if key in ['escape','q']:
            myWin.close()
            core.quit()
        elif key in ['1','2','3','4']:
            if targFlag:
                if (keyTime-targTime)<1:
                    nTargsC=nTargsC+1
                    nTargsH=nTargsH+1
                    targFlag=0
            else:
                nTargsC=nTargsC-1
                nTargsF=nTargsF+1

t = lastFPSupdate = 0
t_p = 0
for i in range(0,(numBlocks)):
    trialClock.reset()
    t_p= 0
    while trialClock.getTime()<(blockLengthOn+blockLengthOff):#for 5 secs
        t=trialClock.getTime()
        t_diff=t-t_p
        if t_diff > fixLength:
            old_color_key = color_key
            fnPrev = fn
            while color_key == old_color_key: 
                fn = np.random.randint(len(my_colors.keys()))
                color_key = list(my_colors.keys())[fn]
            this_color = my_colors[color_key]
            fixation.setColor(this_color)
            if fn>2:
                nTargs = nTargs + 1
                targTime = trialClock.getTime()
                targFlag=1
            t_p = t
        if trialClock.getTime()<blockLengthOn:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge1
            else:
                stim = wedge2
            stim.draw()
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            keyTime=trialClock.getTime()
            if key in ['escape','q']:
                myWin.close()
                core.quit()
            elif key in ['1','2','3','4']:
                if targFlag:
                    if (keyTime-targTime)<1:
                        nTargsC=nTargsC+1
                        nTargsH=nTargsH+1
                        targFlag=0
                else:
                    nTargsC=nTargsC-1
                    nTargsF=nTargsF+1

nTargsC=max(nTargsC,0)
print("nTargs:", int(nTargs))
print("nTargsH:", int(nTargsH))
print("nTargsF:", int(nTargsF))
print("nTargsC:", int(nTargsC))

print("Score: %.2f" % (nTargsC/nTargs*100))


myWin.close()
core.quit()

