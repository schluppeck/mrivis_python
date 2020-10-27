#!/usr/bin/env python
# -*- coding: utf-8 -*-

# original stimulus written by the Silver lab
# psychopy version written by Alex Beckett
# code to try and draw the annulus + counterphase plaid stimuli from Silver 2008
# no targets or anything as yet

from __future__ import division

from psychopy import core, visual, event
from numpy import sin, pi

# Create a window to draw in
win = visual.Window((600, 600), allowGUI=False, monitor='testMonitor', units='deg',blendMode='avg',allowStencil=True)

# Initialize some stimuli
# create the mask we will draw the stimulus through - can only use one so draw one annulus and we will rotate it
mask = visual.RadialStim(win, tex='none', color=1, size=10,
    visibleWedge=[10, 170], radialCycles=4, angularCycles=8, interpolate=False,
    autoLog=False)  # this stim changes too much for autologging to be useful
# gratings for plaid stimulus
grating1 = visual.GratingStim(
    win, tex="sin", mask="circle", texRes=128,
    color='white', size=10, sf=2, ori=45, depth=0.5, opacity=0.5, autoLog=False)
grating2 = visual.GratingStim(
    win, tex="sin", mask="circle", texRes=128,
    color='white', size=10, sf=2, ori=-45, depth=0.5, opacity=0.5, autoLog=False)
# 0 contrats grating + gauss mask to act as target(s)
grating3 =visual.GratingStim(
    win, tex="sin", mask="gauss", texRes=128,pos=(2.5,0), contrast=0,
    color='white', size=4, sf=2, ori=45, opacity=1, autoLog=False)

# gray centre to add fixation to
central_grey = visual.PatchStim(win, tex=None, mask='raisedCos', 
                             color=0,size=1)

message = visual.TextStim(
    win, text='Any key to quit',
    pos=(-0.95, -0.95), units='norm',
    anchorVert='bottom', anchorHoriz='left')

trialClock = core.Clock()
t = 0

# create aperture from mask
aperture = visual.Aperture(win, size=0.9, shape=mask.verticesPix)  # try shape='square'

while not event.getKeys() and t < 20:  # quits after 20 secs
    t = trialClock.getTime()
    # set grating contrast
    grating1.contrast = sin(t * pi * 4)
    grating2.contrast = sin(t * pi * 4)
    
    # initally draw right side
    aperture.ori=0
    aperture.enabled = True  # enabled by default when created
    # draw plaid
    grating1.draw()
    grating2.draw()
    # draw target
    grating3.draw()
    
    # then rorate annulus to draw left
    aperture.ori=180    
    # draw plaid
    grating1.draw()
    grating2.draw()
    
    # release aperture
    aperture.enabled = False  # enabled by default when created
    
    # draw fixation area
    central_grey.draw()
    
    message.draw()

    win.flip()

win.close()
core.quit()
