#!/usr/bin/env python
# eccLoc v1.0

# stimuli for visual hemifield localisation
# input arguments:
# 1 - onLength - How long each eye is stimulated for
# 2 - numBlocks - How many blocks of hemifield stimulation to run for (must be even for equal number of R and L)
# 3 - nullPeriod - how long the blank period at the beginning of the session should run for
# 4 - stimSize - size of the stimulus in proportion to screen height

# parameters can be set using the input arguments above - if the stimulus goes off the edge of the screen, reduce stimSize, or increase if there's dead-space at the edge of the screen.'
# stimulus length = (onLength*numBlocks)+nullPeriod

# parameters can be set either via commnand line arguments or GUI
# if all arguments passed in, assume user is happy with parameters and GUI will not appear

from psychopy import core, visual, event, gui
from numpy import sin, pi
import math,sys,time
import numpy as np

if len(sys.argv)>1:
    onLength=int(sys.argv[1])
else:
    onLength=16

if len(sys.argv)>2:
    numBlocks=int(sys.argv[2])
else:
    numBlocks=10

if len(sys.argv)>3:
    nullPeriod=int(sys.argv[3])
else:
    nullPeriod=onLength/2

if len(sys.argv)>4:
    stimSize=float(sys.argv[4])
else:
    stimSize=1.0
    
if len(sys.argv)>5:
    flashPeriod=float(sys.argv[5])
else:
    flashPeriod=0.25

offLength=10

params = {
        'onLength':onLength,
        'offLength':offLength,
        'numBlocks': numBlocks,
        'nullPeriod': nullPeriod,
        'stimSize': stimSize,
        'flashPeriod': flashPeriod,
        }
tip = {
        'onLength':'length of on blocks',
        'offLength':'length of off blocks',
        'numBlocks': 'number of blocks (centre on/off/surround on/off) to run for',
        'nullPeriod': 'initial rest period',
        'stimSize': 'size of the stimulus in proportion to screen height',
        'flashPeriod': 'flash period (on/off cycle) in s',
        }
params['timeStr']= time.strftime("%b_%d_%H%M", time.localtime())

if len(sys.argv)<5:
    dlg = gui.DlgFromDict(
            dictionary=params,
            title="Eccentricity Localizer",
            fixed=['timeStr'],
            sort_keys=True,
            tip=tip)

    if dlg.OK:
        print(params)
    else:
        core.quit() #user cancelled. quit
else:
    print(params)
    
onLength = params['onLength']
numBlocks = params['numBlocks']
nullPeriod = params['nullPeriod']
stimSize = params['stimSize']

#create a window to draw in
myWin =visual.Window((1280,800),allowGUI=False,
bitsMode=None, units='height', fullscr=1,winType='pyglet',monitor='testMonitor', color=0)
myWin.mouseVisible=False

fixLength=1.0/2
my_colors = {'red':[1,0,0],
             'green':[0,1,0],
             'blue':[0,0,1],
             'yellow':[1,1,0]}

rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi

rotationRate = (1.0/onLength) #revs per sec

#flashPeriod = 0.125 

fixation = visual.ShapeStim(myWin, 
            lineColor='white', 
            lineWidth=2.0, 
            vertices=((-0.5, 0), (0.5, 0), (0,0), (0,0.5), (0,-0.5)), 
            interpolate=False, 
            closeShape=False, 
            pos=(0,0)) 

fixation = visual.PatchStim(myWin, tex=None, mask='circle',sf=0, size=.1,
                            name='fixation', autoLog=False,color=(-1,-1,-1),pos=(0,0))

central_grey = visual.PatchStim(myWin, tex=None, mask='circle', 
                                                    color=0*rgb, 
                                                    size=.2*3)

fixation = visual.PatchStim(myWin, tex=None, mask = 'circle',color=1*rgb,
                                size=.01)#,units='deg')

oneCycle = np.arange(0,1.0, 1/128.0)
oneCycle = np.where(oneCycle<(64/128),1,0)
thisStart=0+0*(64/128)
theseIndices = np.arange(thisStart,thisStart+1,1/128.0)%1.0
theseIndices = (theseIndices*128).astype(np.uint8)
thisMask = oneCycle[theseIndices]

wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful

oneCycle = np.arange(0,1.0, 1/128.0)
oneCycle = np.where(oneCycle<=(64/128),1,0)
thisStart=0+1*(64/128)
theseIndices = np.arange(thisStart,thisStart+1,1/128.0)%1.0
theseIndices = (theseIndices*128).astype(np.uint8)
thisMask = oneCycle[theseIndices]

wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=stimSize,
                           visibleWedge=[0, 360], radialCycles=8, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0),mask=thisMask)#this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=stimSize,
                           visibleWedge=[0, 360], radialCycles=8, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0),mask=thisMask)#this stim changes too much for autologging to be useful

# create text stimuli
message1 = visual.TextStim(myWin, pos=[0,+.5], wrapWidth=1.5, color='#000000', alignText='center', name='topMsg', text="aaa",units='norm')
message2 = visual.TextStim(myWin, pos=[0,-.5], wrapWidth=1.5, color='#000000', alignText='center', name='bottomMsg', text="bbb",units='norm')

# wait for scanner
message1.setText("Please fixate on the central dot during the visual task")
message2.setText("Press a button when you see a yellow dot at fixation")
message1.draw()
message2.draw()
myWin.flip()
event.waitKeys()

kwait = 1
while kwait:
    fixation.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['5','t']:
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
            print(myWin.fps())
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
    while trialClock.getTime()<(2*(onLength+offLength)):#for 5 secs
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
        # set stim type depending on where we are in the cycle
        if trialClock.getTime()<onLength:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge1
            else:
                stim = wedge2
            stim.draw()
        elif trialClock.getTime()<((2*onLength)+offLength) and trialClock.getTime()>(onLength+offLength):
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge3
            else:
                stim = wedge4
            stim.draw()
        
        fixation.draw()

        myWin.flip()
    
        for key in event.getKeys():
            keyTime=trialClock.getTime()
            if key in ['escape','q']:
                print(myWin.fps())
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

message1.setText("Thank you!")
message2.setText("Press 'q' or 'escape' to end the session.")
myWin.clearBuffer() # clear the screen
message1.draw()
message2.draw()
myWin.flip()
thisKey = event.waitKeys(keyList=['q','escape'])

myWin.close()
core.quit()

