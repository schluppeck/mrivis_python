#!/usr/bin/env python
# odcLocCalib v2.0

# stimuli for calibrating stimuli for ODC localisation
# input arguments:
# 1 - blockLength - How long each eye is stimulated for
# 2 - numBlocks - How many blocks of monocular stimulation to run for
# 3 - nullPeriod - how long the blank period between blocks should run for
# 4 - initEye - which eye to start with: 1 =right, -1=left, 2=both
# 5 - stimSize - size of the stimulus in proportion to screen height
# 6 - gyCon - contrast for red eye
# 7 - byCon - contrast for blue eye

from psychopy import visual, event, core, monitors,gui
import math,sys,time


if len(sys.argv)>1:
    blockLength=int(sys.argv[1])
else:
    blockLength=18

if len(sys.argv)>2:
    numBlocks=int(sys.argv[2])
else:
    numBlocks=int(20)

if len(sys.argv)>3:
    nullPeriod=int(sys.argv[3])
else:
    nullPeriod=0

if len(sys.argv)>4:
    stimSize=float(sys.argv[4])
else:
    stimSize=1

if len(sys.argv)>5:
    initEye=float(sys.argv[5])
else:
    initEye=1

if len(sys.argv)>6:
    grCon=float(sys.argv[6])
else:
    grCon=0.5

if len(sys.argv)>7:
    byCon=float(sys.argv[7])
else:
    byCon=0.5

params = {
        'blockLength':blockLength,
        'numBlocks': numBlocks,
        'nullPeriod': nullPeriod,
        'initEye': initEye,
        'stimSize': stimSize,
        'grCon':grCon,
        'byCon':byCon,
        }
params['timeStr']= time.strftime("%b_%d_%H%M", time.localtime())

if len(sys.argv)<10:
    dlg = gui.DlgFromDict(
            dictionary=params,
            title="ODC Localizer",
            fixed=['timeStr'])

    if dlg.OK:
        print(params)
    else:
        core.quit() #user cancelled. quit
else:
    print(params)
    
params['blockLength']=blockLength,
params['numBlocks']=numBlocks,
params['nullPeriod']=nullPeriod,
params['initEye']=initEye,
params['stimSize']=stimSize,
params['grCon']=grCon,
params['byCon']=byCon,


mon = monitors.Monitor('testMonitor',width=58,distance=57)

#create a myWindow to draw in
myWin =visual.Window((1280,800),allowGUI=False,
    bitsMode=None, units='height', winType='pyglet',monitor=mon,fullscr=0, color=0)


    
fixation = visual.ShapeStim(myWin, 
            lineColor='white',
            lineWidth=1,
            vertices=((-0.02, 0), (0.02, 0), (0,0), (0,0.02), (0,-0.02)),
            interpolate=False, 
            closeShape=False, 
            pos=(0,0))

fixation1 = visual.PatchStim(myWin, tex=None, mask='circle',sf=0, size=0.02,
                            name='fixation', autoLog=False,color=(0,0,0),pos=(stimSize*.6,0))

fixation2 = visual.PatchStim(myWin, tex=None, mask='circle',sf=0, size=0.02,
                             name='fixation', autoLog=False,color=(0,0,0),pos=(-stimSize*.6,0))

#INITIALISE SOME STIMULI
dotPatch =visual.DotStim(myWin, color=(1.0,1.0,1.0), dir=270,
    nDots=500, fieldShape='circle', fieldPos=(0.0,0.0),fieldSize=[15],
    dotLife=5, #number of frames for each dot to be drawn
    signalDots='same', #are the signal dots the 'same' on each frame? (see Scase et al)
    noiseDots='walk', #do the noise dots follow random- 'walk', 'direction', or 'position'
    speed=8, coherence=1,dotSize=.25)
#message =visual.TextStim(myWin,text='Hit Q to quit',
#    pos=(0,-0.5))



kwait = 1
while kwait:
    fixation.draw()
    fixation1.draw()
    fixation2.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['5']:
            kwait = 0
        elif key in ['escape','q']:
            print(myWin.fps())
            myWin.close()
            core.quit()
    
#grCon = 0.4
#byCon= 0.7
globalClock = core.Clock()
initialOri=0
wedge1 = visual.RadialStim(myWin, tex='sqrXsqr', color=(grCon,0,0),size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(-stimSize/4,0),colorSpace='rgb')#this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(myWin, tex='sqrXsqr', color=(-grCon,0,0),size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=0,pos=(-stimSize/4,0))#this stim changes too much for autologging to be useful

wedge3 = visual.RadialStim(myWin, tex='sqrXsqr', color=(0,byCon,byCon),size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=180,pos=(stimSize/4,0))#this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(myWin, tex='sqrXsqr', color=(0,-byCon,-byCon),size=stimSize/2,
                           visibleWedge=[0, 360], radialCycles=4, angularCycles=8, interpolate=False,
                           autoLog=False,ori=180,pos=(stimSize/4,0))#this stim changes too much for autologging to be useful

clock=core.Clock()

while clock.getTime()<nullPeriod:#for 5 secs
    fixation.draw()
    #fixation1.draw()
    #fixation2.draw()
    myWin.flip()
    for key in event.getKeys():
        if key in ['escape','q']:
            print(myWin.fps())
            myWin.close()
            core.quit()

t=0
rotationRate = .03 #revs per sec
flashPeriod = 0.2 #seconds for one B-W cycle (ie 1/Hz)

for i in range(0,int(numBlocks/2)):
    clock.reset()
    while clock.getTime()<(blockLength*2):#for 5 secs
        t=globalClock.getTime()
        if clock.getTime()<blockLength:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge1
                stim2= wedge3
            else:
                stim=wedge2
                stim2=wedge4
        else:
            if (t%flashPeriod) < (flashPeriod/2.0):# (NB more accurate to use number of frames)
                stim = wedge3
                stim2 = wedge1
            else:
                stim=wedge4
                stim2 = wedge2

        #stim.setOri(initialOri+(rotDir*t*rotationRate*360.0))
        stim.draw()
        stim2.draw()
        fixation.draw()
        #fixation1.draw()
        #fixation2.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['escape','q']:
                print('rG: ',grCon)
                print('bY: ',byCon)
                print(myWin.fps())
                myWin.close()
                core.quit()
            elif key in '1':
                if grCon < .9:
                    grCon=grCon+.05
                    wedge1.setColor([grCon,0,0])
                    wedge2.setColor([-grCon,0,0])
            elif key in '2':
                if grCon > 0.1:
                    grCon=grCon-.05
                    wedge1.setColor([grCon,0,0])
                    wedge2.setColor([-grCon,0,0])
            elif key in '3':
                if byCon < .9:
                    byCon=byCon+.1
                    wedge3.setColor([0,byCon,byCon])
                    wedge4.setColor([0,-byCon,-byCon])
            elif key in '4':
                if byCon > 0.1:
                    byCon=byCon-.1
                    wedge3.setColor([0,byCon,byCon])
                    wedge4.setColor([0,-byCon,-byCon])
            
clock.reset()
myWin.close()
core.quit()
