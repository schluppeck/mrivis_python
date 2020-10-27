#!/usr/bin/env python
# oriMap v2.0

# stimuli for Ori column localisation, as copied from Yacoub et al 2008
# input arguments:
# 1 - blockLength - How long each 180 rotation lasts for
# 2 - numBlocks - How many cycles to run for
# 3 - nullPeriod - how long the blank period at the beginning of the session should run for
# 4 - stimSize - size of the stimulus in proportion to screen height
# 5 - initDir - rotation direction

# parameters can be set using the input arguments above - if the stimulus goes off the edge of the screen, reduce stimSize, or increase if there's dead-space at the edge of the screen.'
# stimulus length = (blockLength*numBlocks)+nullPeriod

# parameters can be set either via commnand line arguments or GUI
# if all arguments passed in, assume user is happy with parameters and GUI will not appear

from psychopy import core, visual, event, gui
from numpy import sin, pi
import math,sys,time
import numpy as np

if len(sys.argv)>1:
    blockLength=float(sys.argv[1])
else:
    blockLength=60

if len(sys.argv)>2:
    numBlocks=int(sys.argv[2])
else:
    numBlocks=6

if len(sys.argv)>3:
    nullPeriod=int(sys.argv[3])
else:
    nullPeriod=blockLength/2

if len(sys.argv)>4:
    stimSize=float(sys.argv[4])
else:
    stimSize=20

if len(sys.argv)>5:
    initDir=float(sys.argv[5])
else:
    initDir=1

params = {
        'blockLength':blockLength,
        'numBlocks': numBlocks,
        'nullPeriod': nullPeriod,
        'stimSize': stimSize,
        'initDir': initDir
        }
params['timeStr']= time.strftime("%b_%d_%H%M", time.localtime())

print(params)
if len(sys.argv)<6:
    dlg = gui.DlgFromDict(
            dictionary=params,
            title="Visual Localizer",
            fixed=['timeStr'])
    if dlg.OK:
        print(params)
    else:
        core.quit() #user cancelled. quit
else:
    print(params)
    
blockLength = params['blockLength']
numBlocks = params['numBlocks']
nullPeriod = params['nullPeriod']
stimSize = params['stimSize']
initDir = params['initDir']

#create a window to draw in
myWin =visual.Window((1280,800),allowGUI=False,
bitsMode=None, units='deg',fullscr=0, winType='pyglet',monitor='testMonitor', color=0)

fixLength=1.0/2
my_colors = {'red':[1,0,0],
             'green':[0,1,0],
             'blue':[0,0,1],
             'yellow':[1,1,0]}

rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi

rotationRate = (1.0/blockLength) #revs per sec

fixation = visual.ShapeStim(myWin, 
            lineColor='white', 
            lineWidth=2.0, 
            vertices=((-0.5, 0), (0.5, 0), (0,0), (0,0.5), (0,-0.5)), 
            interpolate=False, 
            closeShape=False, 
            pos=(0,0)) 

fixation = visual.PatchStim(myWin, tex=None, mask='circle',sf=0, size=.2,
                            name='fixation', autoLog=False,color=(-1,-1,-1),pos=(0,0))

central_grey = visual.PatchStim(myWin, tex=None, mask='raisedCos', 
                             color=0*rgb,size=1*3)

fixation = visual.PatchStim(myWin, tex=None, mask ='circle',color=1*rgb,
                                size=.4)

#INITIALISE SOME STIMULI
grating1 = visual.GratingStim(myWin,tex="sin",mask="raisedCos",texRes=256,
            color=[1.0,1.0,1.0],colorSpace='rgb', opacity=1.0,
            size=(18,18), sf=(1.0,1.0),
            ori = 0, depth=0.5, phase=0,
            autoLog=False)#this stim changes too much for autologging to be useful

initialOri=0

kwait = 1
while kwait:
    fixation.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['5']:
            kwait = 0
        elif key in ['escape','q']:
            myWin.close()
            core.quit()

clock=core.Clock()

nullOri=initialOri-(initDir*rotationRate*nullPeriod*180)
grating1.setOri(nullOri)

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
respFlag=0;

while trialClock.getTime()<nullPeriod:#for 5 secs
    t=trialClock.getTime()
    t_diff=t-t_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        respFlag = 0
        while color_key == old_color_key: 
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn>2:
            respFlag = 1
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
        t_p = t

    grating1.setOri(nullOri+(t*initDir*rotationRate*180))
    if (t%2<1):
        grating1.setPhase(t*4)
    else:
       grating1.setPhase(t*-4)
    
    fixation.draw()
    myWin.flip()
    
    for key in event.getKeys():
        keyTime=trialClock.getTime()
        if key in ['escape','q']:
            myWin.close()
            core.quit()
        elif key in ['1','2','3','4']:
            if (keyTime-targTime)<1:
                if respFlag:
                    nTargsC=nTargsC+1
                    nTargsH=nTargsH+1
                    respFlag = 0
            elif (keyTime-targTime)>1:
                nTargsC=nTargsC-1
                nTargsF=nTargsF+1

t = lastFPSupdate = 0
t_p = 0

for i in range(0,(numBlocks)):
    trialClock.reset()
    t_p= 0
    while trialClock.getTime()<blockLength:#for 5 secs
        t=trialClock.getTime()
        t_diff=t-t_p
        if t_diff > fixLength:
            old_color_key = color_key
            fnPrev = fn
            respFlag = 0
            while color_key == old_color_key: 
                fn = np.random.randint(len(my_colors.keys()))
                color_key = list(my_colors.keys())[fn]
            this_color = my_colors[color_key]
            fixation.setColor(this_color)
            if fn>2:
                respFlag = 1
                nTargs = nTargs + 1
                targTime = trialClock.getTime()
            t_p = t

        grating1.setOri(initialOri+(t*initDir*rotationRate*180))
        if (t%2<1):
            grating1.setPhase(t*4)
        else:
            grating1.setPhase(t*-4)
        grating1.draw()
        central_grey.draw()
        fixation.draw()

        myWin.flip()
    
        for key in event.getKeys():
            keyTime=trialClock.getTime()
            if key in ['escape','q']:
                myWin.close()
                core.quit()
            elif key in ['1','2','3','4']:
                if (keyTime-targTime)<1:
                    if respFlag:
                        nTargsC=nTargsC+1
                        nTargsH=nTargsH+1
                        respFlag = 0
                elif (keyTime-targTime)>1:
                    nTargsC=nTargsC-1
                    nTargsF=nTargsF+1

trialClock.reset()
t_p=0;
while trialClock.getTime()<nullPeriod:#for 5 secs
    t=trialClock.getTime()
    t_diff=t-t_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        respFlag = 0
        while color_key == old_color_key: 
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn>2:
            respFlag = 1
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
        t_p = t

    grating1.setOri(nullOri+(t*initDir*rotationRate*180))
    if (t%2<1):
        grating1.setPhase(t*4)
    else:
       grating1.setPhase(t*-4)
    #grating1.draw()
    fixation.draw()

    myWin.flip()
    
    for key in event.getKeys():
        keyTime=trialClock.getTime()
        if key in ['escape','q']:
            myWin.close()
            core.quit()
        else:
            if (keyTime-targTime)<1:
                if respFlag:
                    nTargsC=nTargsC+1
                    nTargsH=nTargsH+1
                    respFlag = 0
            elif (keyTime-targTime)>1:
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

