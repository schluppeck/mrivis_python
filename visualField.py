#!/usr/bin/env python

# stimuli for measuring visual field coverage
# original code by jwp
# updated for PsychoPy3 by ab
# can use saved values in retinotopy.py

from psychopy import visual, event, core, monitors, gui, misc
from psychopy import monitors
import scipy

try:
    #try to load previous info
    visField = misc.fromFile('visualFieldParams.pickle')
except:
    #if no file use some defaults
    visField = {'centre':scipy.array((0.0,0.0)),
        'size':6.0}

myMon=monitors.Monitor('testMonitor')
scrSize=myMon.getSizePix()

#create a window to draw in
myWin = visual.Window(scrSize, monitor=myMon, allowGUI=False, units='deg')

#INITIALISE SOME STIMULI

fixSpot = visual.PatchStim(myWin,tex="none", mask='gauss', pos=(0,0), size=(0.5,0.5),color=[-1.0,-1.0,-1.0])
surr = visual.PatchStim(myWin,pos=visField['centre'],
                        color=1,
                        tex="None",mask="circle",texRes=512,
                        size=visField['size'], opacity=0.50, interpolate=True)
center = visual.PatchStim(myWin,pos=visField['centre'],
                          color=-1,
                          tex="None",mask="circle",texRes=512,
                          size=visField['size']-0.3, opacity=0.2, interpolate=True)
stimSize=surr.size; stimPos=surr.pos
status = visual.TextStim(myWin,pos=stimPos,
                         text='test')

message1 = visual.TextStim(myWin,units='norm', color=-1, pos=(-0.9,0.9),alignHoriz='left',
                           text='Testing:%s' %myMon.name)
message2 = visual.TextStim(myWin,units='norm', color=-1, pos=(-0.9,0.75),alignHoriz='left',
                           text='Mouse controls pos and size. Hit q to quit')
myMouse = event.Mouse(win=myWin)
myMouse.setPos([200,200])
carryOn=True
while carryOn:#quits after 20 secs
    #handle key presses each frame
    #get mouse events
    mouse_dX,mouse_dY = myMouse.getRel()
    mouse1, mouse2, mouse3 = myMouse.getPressed()
    
    if mouse3:
        surr.setSize(mouse_dX/5.0, '+')
        center.setSize(mouse_dX/5.0, '+')
    elif mouse1:
        surr.setPos((mouse_dX, mouse_dY), '+')
        center.setPos((mouse_dX, mouse_dY), '+')
    
    #update status text
    stimSize=surr.size; stimPos = surr.pos; 
    status.setPos(stimPos)
    status.setText('x=%.1f, y=%.1f, r=%.1f' %(stimPos[0], stimPos[1], stimSize[0]/2))
    
    
    fixSpot.draw()
    surr.draw()
    center.draw()
    status.draw()
    message1.draw()
    message2.draw()
    
    myWin.update()#redraw the buffer
    
    for key in  event.getKeys():
        if key in ['escape','q']:
            carryOn=False
            
    event.clearEvents()

myWin.close()
saveDlg = gui.Dlg('Save params')
saveDlg.addText('Save params to file? (cancel to leave previous params)')
wasOk = saveDlg.show()
if saveDlg.OK:
    misc.toFile('visualFieldParams.pickle', {'size': surr.size[0],'centre_x': surr.pos[0],'centre_y': surr.pos[1]})
    print('Fixation=%.2f,%.2f; Size(radius)=%.2f   [SAVED]' %(surr.pos[0], surr.pos[1], surr.size[0]/2.0))
else:
    print('Fixation=%.2f,%.2f; Size(radius)=%.2f   [not saved]' %(surr.pos[0], surr.pos[1], surr.size[0]/2.0))
    
core.quit()
