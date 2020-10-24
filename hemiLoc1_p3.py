#!/usr/bin/env python

from psychopy import core, visual, event
from numpy import sin, pi
import math,sys
import numpy as np


blockLength=16
numBlocks=10
nullPeriod=5
stimSize=1
initDir=1
#create a window to draw in
myWin =visual.Window([800,800],units='height')
#,allowGUI=False,
#bitsMode=None, units='height', fullscr=1,winType='pyglet',monitor='testMonitor', color=0)

fixLength=1.0/2
my_colors = {'red':[1,0,0],
             'green':[0,1,0],
             'blue':[0,0,1],
             'yellow':[1,1,0]}
rgb = np.array([1.,1.,1.])
two_pi = 2*np.pi
rotationRate = (1.0/blockLength) #revs per sec
flashPeriod = 0.125 

central_grey = visual.PatchStim(myWin, tex=None, mask='circle', 
                                                    color=0*rgb, 
                                                    size=.2*3)

fixation = visual.PatchStim(myWin, tex=None, mask = 'circle',color=1*rgb,
                                size=0.1)

wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=stimSize,
                           visibleWedge=[5, 175], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=stimSize,
                           visibleWedge=[5, 175], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful

wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=1,size=stimSize,
                           visibleWedge=[5,175], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=-1,size=stimSize,
                           visibleWedge=[5,175], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful

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

#nullOri=initialOri-(initDir*rotationRate*nullPeriod*180)
#grating1.setOri(nullOri)

color_key = 'white'
fn = 0;
trialClock = core.Clock()

t = lastFPSupdate = 0
t_p = 0

nTargs = 0.;
nTargsC = 0.;
nTargsF = 0.;
targTime= 1000;

while trialClock.getTime()<nullPeriod:#for 5 secs
    t=trialClock.getTime()
    t_diff=t-t_p
#    if t_diff > fixLength:
#        old_color_key = color_key
#        fnPrev = fn
#        while color_key == old_color_key: 
#            fn = np.random.randint(len(my_colors.keys()))
#            color_key = 'white'
#        this_color = my_colors[color_key]
#        fixation.setColor(this_color)
#        if fn>2:
#            
#            nTargs = nTargs + 1
#            targTime = trialClock.getTime()
#        t_p = t
#        
    fixation.draw()

    myWin.flip()
    
    for key in event.getKeys():
        keyTime=trialClock.getTime()
        if key in ['escape','q']:
            
            myWin.close()
            core.quit()
        else:
            if (keyTime-targTime)<1:
                nTargsC=nTargsC+1
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
#        if t_diff > fixLength:
#            old_color_key = color_key
#            fnPrev = fn
#            while color_key == old_color_key: 
#                fn = np.random.randint(len(my_colors.keys()))
#                color_key = my_colors.keys()[fn]
#            this_color = my_colors[color_key]
#            fixation.setColor(this_color)
#            if fn>2:
#            
#                nTargs = nTargs + 1
#                targTime = trialClock.getTime()
#            t_p = t

        if trialClock.getTime()<blockLength/2:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge1
            else:
                stim = wedge2
        else:
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
                
                myWin.close()
                core.quit()
            else:
                if (keyTime-targTime)<1:
                    nTargsC=nTargsC+1
                elif (keyTime-targTime)>1:
                    nTargsC=nTargsC-1
                    nTargsF=nTargsF+1

#print "nTargsC:", int(nTargsC)
#print "nTargs:", int(nTargs)
#print "nTargsF:", int(nTargsF)
#print "Score: %.2f" % (nTargsC/nTargs*100)

myWin.close()
core.quit()

