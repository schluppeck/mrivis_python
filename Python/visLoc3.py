# stimuli for PVC localisation, as copied from checker_3 (Vu)
# input arguments:
# 1 - blockLength - How long each on/off block lasts
# 2 - numBlocks - How many cycles of on/off to run for
# 3 - nullPeriod - how long the blank period at the beginning of the session should run for
# 4 - stimSize - size of the stimulus in proportion to screen height
# 5 - initEye - which eye to start with: 1 =right, -1=left
#!/usr/bin/env python
import numpy as np
from psychopy import visual, event, core, monitors
import math,sys

my_colors = {'red':[1,0,0],
                     'yellow':[1,1,0],
                     'green':[0,1,0],
                     'blue':[0,0,1]}
#                     'm1':[1,1,0],
#                     'm2':[0,0.6,0.6],
#                     'm3':[0,0.6,0],
#                     'm4':[0.6,0.6,0],
#                     'm5':[0,0,0.6],
#                     'm6':[0.6,0.6,1]}

fixLength=.14
rgb = np.array([1.,1.,1.])


if len(sys.argv)>1:
    blockLength=int(sys.argv[1])
else:
    blockLength=48

if len(sys.argv)>2:
    numBlocks=int(sys.argv[2])
else:
    numBlocks=8

if len(sys.argv)>3:
    nullPeriod=int(sys.argv[3])
else:
    nullPeriod=blockLength

if len(sys.argv)>4:
    stimSize=float(sys.argv[4])
else:
    stimSize=.3

if len(sys.argv)>5:
    initEye=float(sys.argv[5])
else:
    initEye=1

mon = monitors.Monitor('testMonitor',width=58,distance=57)

#create a myWindow to draw in
myWin =visual.Window((1280,800),allowGUI=False,
    bitsMode=None, units='height', winType='pyglet',monitor=mon,fullscr=1, color=0)


    
fixation = visual.ShapeStim(myWin, 
            lineColor='white',
            lineWidth=.20,
            vertices=((-0.02, 0), (0.02, 0), (0,0), (0,0.02), (0,-0.02)),
            interpolate=False, 
            closeShape=False, 
            pos=(0,0))


fixation = visual.PatchStim(myWin, tex=None, mask = 'circle',color=1*rgb,
                                size=0.02)

#fixation2 = visual.PatchStim(myWin, tex=None, mask='gauss',sf=0, size=0.05,
#                             name='fixation', autoLog=False,color=(1,0,0),pos=(-stimSize*.6,0))

#INITIALISE SOME STIMULI
#dotPatch =visual.DotStim(myWin, color=(1.0,1.0,1.0), dir=270,
#    nDots=500, fieldShape='circle', fieldPos=(0.0,0.0),fieldSize=[15],
#    dotLife=5, #number of frames for each dot to be drawn
#    signalDots='same', #are the signal dots the 'same' on each frame? (see Scase et al)
#    noiseDots='walk', #do the noise dots follow random- 'walk', 'direction', or 'position'
#    speed=8, coherence=1,dotSize=.25)
#message =visual.TextStim(myWin,text='Hit Q to quit',
#    pos=(0,-0.5))



kwait = 1
while kwait:
#    fixation.draw()
    fixation.draw()
    #fixation2.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['5']:
            kwait = 0
        elif key in ['escape','q']:
            print myWin.fps()
            myWin.close()
            core.quit()
    

globalClock = core.Clock()
initialOri=0
color_key = 'white'
fn = 0
t_f=0
t_f_p=0

nTargs = 0.
nTargsC = 0.
nTargsF = 0.
targTime= 1000

wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=stimSize,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=stimSize,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful

wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=0,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=0,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful

trialClock=core.Clock()

while trialClock.getTime()<nullPeriod:#for 5 secs
    t=trialClock.getTime()
    t_diff=t-t_f_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        while color_key == old_color_key: 
            fn = np.random.randint(len(my_colors.keys()))
            color_key = my_colors.keys()[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn>2:
            
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
        t_f_p = t
    fixation.draw()

    myWin.flip()
    
    for key in event.getKeys():
        keyTime=trialClock.getTime()
        if key in ['escape','q']:
            print myWin.fps()
            myWin.close()
            core.quit()
        else:
            if (keyTime-targTime)<1:
                nTargsC=nTargsC+1
            elif (keyTime-targTime)>1:
                nTargsC=nTargsC-1
                nTargsF=nTargsF+1

t=0
rotationRate = .03 #revs per sec
flashPeriod = 0.067 #seconds for one B-W cycle (ie 1/Hz)

for i in range(0,(numBlocks/2)):
    trialClock.reset()
    while trialClock.getTime()<(blockLength*2):#for 5 secs
        t=trialClock.getTime()
        if trialClock.getTime()<blockLength:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge1
            else:
                stim = wedge2
        else:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge3
            else:
                stim = wedge4
        t_f=trialClock.getTime()
        t_f_diff = t_f-t_f_p
        if t_f_diff > fixLength:
            old_color_key = color_key
            while color_key == old_color_key: 
                color_key = my_colors.keys()[np.random.randint(len(my_colors.keys()))]
            this_color = my_colors[color_key]
            fixation.setColor(this_color)
            t_f_p=t_f
        #stim.setOri(initialOri+(rotDir*t*rotationRate*360.0))
        stim.draw()
#        fixation.draw()
        fixation.draw()
#        fixation2.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                print myWin.fps()
                myWin.close()
                core.quit()
                
trialClock.reset()


    
myWin.close()
core.quit()
#            
#            
#            
#    #handle key presses each frame
#    for key in event.getKeys():
#        if key in ['escape','q']:
#            print myWin.fps()
#            myWin.close()
#            core.quit()
#    event.clearEvents('mouse')#only really needed for pygame myWindows
#
