#!/usr/bin/env python

# stimuli for retinotopic mapping
# original code by jwp
# updated for PsychoPy3 by ab
# can measure vf centre and coverage usin visualField.py

import time, scipy, os 
from psychopy import visual, event, core, monitors, gui, misc
from psychopy import hardware
import numpy as num

#last run of visual field
try:
    #try to load previous info
    visField = misc.fromFile('visualFieldParams.pickle')
except:
    #if no file use some defaults
    visField = {'centre_x':0.,
        'centre_y':0.,
        'size':6.0}

#last run of retinotopy
try:
    #try to load previous info
    params = misc.fromFile('retinotopyParams.pickle')
except:
    #if no file use some defaults
    params = {
        'observer':'jwp',
        'direction': 'exp',
        'cycleTime': 24,
        'nCycles': 10,        
        'dutyCycleWedge':0.125,
        'dutyCycleAnn':0.25,
        }

#set some more that don't change
params['timeStr']= time.strftime("%b_%d_%H%M", time.localtime())
params['size'] = float(visField['size'])
params['centre_x']=visField['centre_x']
params['centre_y']=visField['centre_y']


dlg = gui.DlgFromDict(
        dictionary=params,
        title="Retinotopy",
        fixed=['timeStr'])

if dlg.OK:
    misc.toFile('retinotopyParams.pickle',params)
else:
    core.quit() #user cancelled. quit

print("Observer:%s, run:%s, time:%s" %(params['observer'], params['direction'], params['timeStr']))

DEBUG=True

if DEBUG:
    winSize=(1024,768)
    myWin = visual.Window(size=winSize, monitor='testMonitor',bitsMode=None,
        allowGUI=True, units='deg')
else:
    winSize=(1024,768)
    myWin = visual.Window(size=winSize, monitor='testMonitor',
                          units='deg',bitsMode=None,
                          allowGUI=False,
                          fullscr=1)

class SlidingAnnulus:
    def __init__(self, window,
                 size,pos =[0,0],
                 dutyCycle=0.25,
                 nRings=4,
                 angularRate=1, #phase shift per frame (degs)
                 changeProb=0.01, #percentage of frames on which dir changes
                 ):
        self.rings=[]
        self.ringWidth = dutyCycle/nRings
        self.angularRate = angularRate
        self.changeProb = changeProb
        self.nRings = nRings
        self.pos=pos
        self.size = size
        self.radialPhase=0
        self._oneCycle = num.arange(0,1.0, 1/128.0)
        self._oneCycle = num.where(self._oneCycle<=self.ringWidth,1,0)
        for n in range(nRings):
            thisStart=self.radialPhase+n*self.ringWidth
            theseIndices = num.arange(thisStart,thisStart+1,1/128.0)%1.0
            theseIndices = (theseIndices*128).astype(num.uint8)
            thisMask = self._oneCycle[theseIndices]
            thisRing = visual.RadialStim(window,pos=self.pos,
                            angularRes=360, 
                            radialCycles=0, angularCycles=16,
                            size=self.size, texRes=64,mask=thisMask,                            
                            )
            self.rings.append(thisRing)
        
    def draw(self):
        for thisRing in self.rings:
            thisRing.draw()
    
    def setOri(self, ori):
        for thisRing in self.rings:
            thisRing.setOri(ori)
    
    def incrementRotation(self):
        if num.random.random()<self.changeProb:
            self.angularRate *= (-1) #flip the direction by negating the rate
        for n, ring in enumerate(self.rings):#alternate segments go in and out
            if n%2==0: ring.setOri(self.angularRate,'+')
            else: ring.setOri(self.angularRate,'-')
            
    def setPhase(self, phase):	
        self.radialPhase = phase
        for n,thisRing in enumerate(self.rings):
            thisStart=self.radialPhase+n*self.ringWidth
            theseIndices = num.arange(thisStart,thisStart+1.001,1/63.0)%1.0
            theseIndices = (theseIndices*128).astype(num.uint8)
            thisMask = self._oneCycle[theseIndices]
            thisRing.setMask(thisMask)
    
class SlidingWedge:
    def __init__(self, window,size, pos,
            dutyCycle=0.125,
            nSegs=3,
            radialRate=0.05, #phase shift per frame (fraction of a cycle)
            changeProb=0.01, #percentage of frames on which dir changes
            ):
        self.segments=[]
        self.segWidth = dutyCycle*360.0/nSegs
        self.radialRate = radialRate
        self.changeProb = changeProb
    
        phase=0
        for n in range(nSegs):
            thisSeg = visual.RadialStim(window, pos=pos,angularRes=360,
                        radialCycles=6, angularCycles=0,
                        visibleWedge=[n*self.segWidth, (n+1)*self.segWidth],
                        size=size, texRes=64,mask=[0.5]
                        )
            self.segments.append(thisSeg)
    
    def draw(self):
        for thisSeg in self.segments:
            thisSeg.draw()
    
    def setOri(self, ori):
        for thisSeg in self.segments:
            thisSeg.setOri(ori)
    
    def incrementPhase(self):
        if num.random.random()<self.changeProb:
            self.radialRate *= (-1) #flip the direction by negating the rate
        for n, seg in enumerate(self.segments):#alternate segments go in and out
            if n%2==0: seg.setRadialPhase(self.radialRate,'+')
            else: seg.setRadialPhase(self.radialRate,'-')
        
    def setMask(self,newmask):
        for thisSeg in self.segments:
            thisSeg._set('mask',newmask)
    
params['centre']=num.array((params['centre_x'],params['centre_y']))
    
if params['direction'] in ['cw','ccw']:
    #create an instance of our wedge
    wedge = SlidingWedge(myWin, pos = params['centre'], size=params['size'],
                         dutyCycle=params['dutyCycleWedge'])
else:
    annulus = SlidingAnnulus(myWin, pos=params['centre'], size=params['size'],
                             dutyCycle=params['dutyCycleAnn'])
#always need a fixation point
fixation = visual.PatchStim(myWin, mask='circle',tex=None, 
                            size=0.1, pos=params['centre'])

#get rotation speed in deg/sec
if params['direction'] == 'cw':
    cycleSpeed = 360.0/params['cycleTime']
elif params['direction']=='ccw':
    cycleSpeed = -360.0/params['cycleTime']
elif params['direction']=='exp':
    cycleSpeed = -1.0/params['cycleTime']
elif params['direction']=='con':
    cycleSpeed = 1.0/params['cycleTime']
    
def quit():
    print('user quit before end of run')
    myWin.close()
    core.quit()
    
#update and wait for the go signal
myWin.update()
event.waitKeys()#check for scanner pulse or keypress
        
globalClock = core.Clock();g=0
lastSwitch=globalClock.getTime()

while g<params['cycleTime']*params['nCycles']:
    g=globalClock.getTime()
    
    if params['direction'] in ['cw','ccw']:
        wedge.incrementPhase()
        wedge.setOri(cycleSpeed*g)
        wedge.draw()
    
    elif params['direction'] in ['exp','con']:
        annulus.incrementRotation()
        annulus.setPhase((cycleSpeed*g)%1)
        annulus.draw()
        
    fixation.draw()
    myWin.update()
    for key in event.getKeys():
        if key in['escape', 'q']:
            quit()
            
print('%%%%%%%%%%%%%%%%%')
print("completed %s run. t=%.2f. meanFPS=%.1f" %(params['direction'], globalClock.getTime(), myWin.fps()))
print('%%%%%%%%%%%%%%%%%')
core.quit()