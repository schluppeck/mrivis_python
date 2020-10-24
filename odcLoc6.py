# stimuli for ODC localisation, as copied from Yacoub et al 2007
# input arguments:
# 1 - blockLength - How long each eye is stimulated for
# 2 - numBlocks - How many blocks of monocular stimulation to run for
# 3 - blankPeriod - how long the blank period between blocks should run for
# 4 - initEye - which eye to start with: 1 =right, -1=left, 2=both
# 5 - stimSize - size of the stimulus in proportion to screen height
# 6 - gyCon - contrast for red eye
# 7 - byCon - contrast for blue eye
# 8 - annulSize - size of the fixation annulus relative to stim
#!/usr/bin/env python
from psychopy import visual, event, core, monitors
import math,sys


if len(sys.argv)>1:
    blockLength=float(sys.argv[1])
else:
    blockLength=4

if len(sys.argv)>2:
    numBlocks=int(sys.argv[2])
else:
    numBlocks=6

if len(sys.argv)>3:
    blankPeriod=float(sys.argv[3])
else:
    blankPeriod=blockLength

if len(sys.argv)>4:
    initEye=float(sys.argv[4])
else:
    initEye=1

if len(sys.argv)>5:
    stimSize=float(sys.argv[5])
else:
    stimSize=1

if len(sys.argv)>6:
    grCon=float(sys.argv[6])
else:
    grCon=1

if len(sys.argv)>7:
    byCon=float(sys.argv[7])
else:
    byCon=1

if len(sys.argv)>8:
    annulSize=float(sys.argv[8])
else:
    annulSize=0.125
    
if len(sys.argv)>9:
    initBlank=float(sys.argv[9])
else:
    initBlank=0

mon = monitors.Monitor('testMonitor',width=58,distance=57)

#create a myWindow to draw in
myWin =visual.Window((1280,800),allowGUI=False,
    bitsMode=None, units='height', winType='pyglet',monitor=mon,fullscr=1, color=0)


    
fixation = visual.ShapeStim(myWin, 
            lineColor='white',
            lineWidth=1,
            vertices=((-0.02, 0), (0.02, 0), (0,0), (0,0.02), (0,-0.02)),
            interpolate=False, 
            closeShape=False, 
            pos=(0,0))

annul= visual.RadialStim(myWin, tex='sqrXsqr', color=(0,0,0),size=stimSize*annulSize,
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
            print myWin.fps()
            myWin.close()
            core.quit()
    
fixation.setLineColor('black')

globalClock = core.Clock()
initialOri=0

wedgeB1 = visual.RadialStim(myWin, tex='sqrXsqr', color=(1,1,1),size=stimSize,
                       visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                       autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
wedgeB2 = visual.RadialStim(myWin, tex='sqrXsqr', color=(-1,-1,-1),size=stimSize,
                       visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                       autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful

wedgeL1 = visual.RadialStim(myWin, tex='sqrXsqr', color=(grCon,0,0),size=stimSize,
                       visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                       autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
wedgeL2 = visual.RadialStim(myWin, tex='sqrXsqr', color=(-grCon,0,0),size=stimSize,
                       visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                       autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful

wedgeR1 = visual.RadialStim(myWin, tex='sqrXsqr', color=(0,byCon,byCon),size=stimSize,
                       visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                       autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful
wedgeR2 = visual.RadialStim(myWin, tex='sqrXsqr', color=(0,-byCon,-byCon),size=stimSize,
                       visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                       autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful
#elif initEye==-1:
#    wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=(grCon,0,0),size=stimSize,
#                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
#                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
#    wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=(-grCon,0,0),size=stimSize,
#                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
#                           autoLog=False,ori=0,pos=(0,0))#this stim changes too much for autologging to be useful
#
#    wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=(0,byCon,byCon),size=stimSize,
#                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
#                           autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful
#    wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=(0,-byCon,-byCon),size=stimSize,
#                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
#                           autoLog=False,ori=180,pos=(0,0))#this stim changes too much for autologging to be useful



clock=core.Clock()

#while clock.getTime()<nullPeriod:#for 5 secs
#    fixation.draw()
#    fixation1.draw()
#    fixation2.draw()
#    myWin.flip()
#    for key in event.getKeys():
#        if key in ['escape','q']:
#            print myWin.fps()
#            myWin.close()
#            core.quit()

t=0
rotationRate = .03 #revs per sec
flashPeriod = 0.2 #seconds for one B-W cycle (ie 1/Hz)
whichEye=initEye

clock.reset()
while clock.getTime()<initBlank:#for 5 secs
    fixation.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['escape','q']:
            print myWin.fps()
            myWin.close()
            core.quit()

if whichEye == 2:
    clock.reset()
    while clock.getTime()<(blockLength):#for 5 secs
        t=globalClock.getTime()
        if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
            stim = wedgeB1
        else:
            stim = wedgeB2
        stim.draw()
        annul.draw()
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                print myWin.fps()
                myWin.close()
                core.quit()
    clock.reset()
    while clock.getTime()<blankPeriod:#for 5 secs
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                print myWin.fps()
                myWin.close()
                core.quit()
    whichEye=1;

for i in range(0,numBlocks):
    clock.reset()
    while clock.getTime()<(blockLength):#for 5 secs
        t=globalClock.getTime()
        if whichEye == 1:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedgeL1
            else:
                stim = wedgeL2
        elif whichEye == -1:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedgeR1
            else:
                stim = wedgeR2

        #stim.setOri(initialOri+(rotDir*t*rotationRate*360.0))
        stim.draw()
        annul.draw()
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                print myWin.fps()
                myWin.close()
                core.quit()
    whichEye=whichEye*-1
    clock.reset()
    while clock.getTime()<blankPeriod:#for 5 secs
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                print myWin.fps()
                myWin.close()
                core.quit()
clock.reset()


    
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
