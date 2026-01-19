# compatibility layer
# making sure we have a consistent interface across
# all different scripts in this folder.
#
# this can also contain some site-specific parameters.
#
# 2025-05-05, ds

# import psychopy
from html import parser
from tqdm import tqdm
import PIL.ImageOps
from scipy.io import savemat
from psychopy import core, visual, event, plugins, session, gui
from psychopy import __version__ as PSYCHOPY_VERSION
import os
import sys
import argparse
import time
import numpy as np
from inspect import getframeinfo, stack


def debuginfo(message):
    """ Print debug info with file name and line number.
    """
    caller = getframeinfo(stack()[-1][0])
    # python3 syntax print
    print("%s:%d - %s\n" %
          (os.path.basename(caller.filename), caller.lineno, message))


def todo(message=None, exit=False):
    print("\033[32m")
    print("(TODO!) ")
    debuginfo(message)
    print("\033[0m")
    if exit:
        print("Exiting...")
        core.quit()


def setDefaultParams():
    """ Set default parameters for the setup

    Returns a dict with the parameters (which can be modified if
    e.g. device is not available, or specific to each expt.)
    """
    params = {}

    # try to connect to VPixx device
    params['USE_VPIXX'] = True

    # default parameters
    # if true, make a small, non-fullscreen window for coding
    params['CODING_WINDOW'] = False
    params['SCREEN_SIZE'] = np.array([1920, 1080])  # size of the screen
    params['CHECK_TIMING'] = False

    # FIXATION stuff, set defaults here.
    params['FIXATION_INFO'] = {
        'nTargsH': 0,
        'nTargs': 0,
        'nTargsC': 0,
        'nTargsF': 0,
        'targTime': 1000,
        'targFlag': 0,
        'color_key': 'white',
        'fn': 0,
        'targetType': 'cross',  # or 'circle'
        'fixationSize': 0.05,
        'fixationLineWidth': 8.0,
        'my_colors': {'red': [1, 0, 0],
                      'green': [0, 1, 0],
                      'blue': [0, 0, 1],
                      'yellow': [1, 1, 0]},  # target color
        'fixLength': 1.0 / 2
    }
    params['BUTTON_CODES'] = ['1', '2', '3', '4']  # keyboard. fix for VPIXX.

    # allow interruptions for screen capture
    params['ALLOW_PAUSE'] = True
    params['PAUSE_KEY'] = 'p'
    params['PAUSE_TIME'] = 10  # seconds for e.g screen caputre

    return params


def getParamsGUI(args, params):
    """ Get parameters from GUI.

    Merges command line args with params dict and shows GUI.
    """
    # update params with any command line args
    for key in args.keys():
        if key in params.keys():
            params[key] = args[key]

    # some parameters should not be changed
    keys_to_pop = ['FIXATION_INFO', 'PAUSE_KEY', 'PAUSE_TIME',
                   'BUTTON_CODES']
    for key in keys_to_pop:
        params.pop(key, None)

    # open up GUI to adjust parameters
    dlg = gui.DlgFromDict(
        dictionary=params,
        title="Experiment Parameters"
    )
    if not dlg.OK:
        print("User cancelled from GUI.")
        core.quit()

    print(dlg.data)
    params.update(dlg.data)
    return params


def updateParamsFromArgs(params, args):
    """ Update params dict from command line args.

    Merges command line args with params dict.
    """
    # update params with any command line args
    params.update(args)
    # print(params)
    return params


def loadVPixxLib(params=None):
    """ Load the VPixx library if available.

    Tries to import pypixxlib and set up the device.
    Fails gracefully if not available.
    """

    assert params is not None, "params dict must be provided"

    if params['USE_VPIXX']:
        try:
            import pypixxlib
            # digital IO, triggering

            from pypixxlib.propixx import PROPixxCTRL
            # digital IO, triggering
            # if you have a datapixx3 change this to “from pypixxlib.datapixx import DATAPixx3”
            from pypixxlib.propixx import PROPixxCTRL
            print("(compatibility) using pypixxlib")
        except ImportError:
            print("(compatibility) pypixxlib not found. Need this for triggers. etc")
            pypixxlib = None
            print("Exiting... for now - @TODO emulation mode!!?")
            core.quit()
    else:
        print("(compatibility) not using VPIXX support as per user request.")
        print("\033[31mWarning: continuing without VPIXX support\033[0m")


def getVPixxDevice(params):
    """Open the VPixx device.

    Making this a function, so we can emulate if needed later on.
    """
    if params['USE_VPIXX']:
        try:
            myDevice = PROPixxCTRL()
        except Exception as e:
            print("No PROPixx found?", e)
            sys.exit(1012)
    else:
        # debugging away from VPIXX or coding elsewhere...
        myDevice = None

    return myDevice


def versionCheck():
    """
    Check the version of psychopy and return True if it's modern (>= 2020.1.0)
    """
    if str(PSYCHOPY_VERSION) < '2020.1.0':
        print("(compatibility) running an older version of psychopy")
        return False
    else:
        print(
            f"\n(compatibility) modern version of psychopy. version: {PSYCHOPY_VERSION}")
        psychopy_modern = True
        plugins.activatePlugins()  # needed for modern version
        # PatchStim migrated to GratingStim in newer version
        visual.PatchStim = visual.GratingStim
        return True


def setupParser(description=None, useDefaults=True):
    parser = argparse.ArgumentParser(
        prog=sys.argv[0])

    # set up some defaults that should work across alls scripts
    if useDefaults:
        # allow user to specify --vpixx True/False at command line...
        # --vpixx and --no-vpixx options
        parser.add_argument('--vpixx', dest='USE_VPIXX', action='store_true',
                            help='use VPIXX device')
        parser.add_argument('--no-vpixx', dest='USE_VPIXX',
                            action='store_false', help='run without VPIXX device (eg for testing)')
        # as well as coding window, etc.
        parser.add_argument('--coding-window', dest='CODING_WINDOW',
                            action='store_true',
                            help='use small debug window for coding')
        parser.add_argument('--screen-size', dest='SCREEN_SIZE',
                            type=int, nargs=2,
                            help='screen size as width height')
        parser.add_argument('--check-timing', dest='CHECK_TIMING', action='store_true',
                            help='check screen timing (false on MacOS: buggy timing!)')
        parser.add_argument('--use-gui', dest='USE_GUI', action='store_true',
                            help='use GUI to set parameters (overrides command line args)')
        parser.set_defaults(USE_VPIXX=True,
                            CODING_WINDOW=False,
                            SCREEN_SIZE=[1920, 1080],
                            CHECK_TIMING=False,
                            USE_GUI=False)

    if description is not None:
        parser.description = description

    return parser


def reconcileParamsAndArgs(params, args):
    """ Reconcile params dict and args dict.

    Merges command line args with params dict and shows GUI.

    On windows, opens GUI and on Linux/MacOS uses command line args.
    Then merges settings back into params dict to further use

    """
    # and for the WINDOWS version, we really want a GUI!
    if sys.platform.startswith('win'):
        print(
            "\033[31m(reconcileParamsAndArgs) On Windows, prefer use of GUI\033[0m")
        print("                         opening up GUI then adjusting params with args...")
        params = getParamsGUI(args, params)

    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        print("(reconcileParamsAndArgs) On Linux/MacOS, command line args are fine.")
        if args['USE_GUI']:
            print(
                "\033[31m(reconcileParamsAndArgs) User requested GUI use -- opening GUI\033[0m")
            params = getParamsGUI(params, args)
        else:
            # update params with any command line args
            print(".                        adjusting params with args...")
            params = updateParamsFromArgs(params, args)

    else:
        print("\033[31m(reconcileParamsAndArgs) Unknown platform!!\033[0m")
        core.quit()

    return params


def createWindow(units='height', params=None):
    """
    Create a window for the experiment.

    Default units are in height.
    Picks up other GLOBAL settings from the file here!
    """
    assert params is not None, "params dict must be provided"

    SCREEN_SIZE = np.array(params['SCREEN_SIZE'])
    CODING_WINDOW = params['CODING_WINDOW']
    CHECK_TIMING = params['CHECK_TIMING']

    # create window, taking into account debug choices
    fullscr = False if CODING_WINDOW else True
    allowGUI = True if CODING_WINDOW else False
    pos = (50, 50) if CODING_WINDOW else None

    myWin = visual.Window(SCREEN_SIZE,
                          allowGUI=allowGUI,
                          bitsMode=None,
                          checkTiming=CHECK_TIMING,
                          color=0,
                          fullscr=fullscr,
                          monitor='testMonitor',
                          pos=pos,
                          units=units,
                          winType='pyglet')  # flip X
    return myWin


def createFixation(myWin, fixationInfo=None):
    """
    Create a fixation target for the experiment.
    """
    assert fixationInfo is not None, "fixationInfo dict must be provided"
    # create fixation / using defaults if not passed in!

    fixationLineWidth = fixationInfo['fixationLineWidth']
    fixationSize = fixationInfo['fixationSize']

    if fixationInfo['targetType'] == 'circle':
        fixation = visual.PatchStim(myWin, tex=None, mask='circle', sf=0,
                                    size=fixationSize,
                                    name='fixation', autoLog=False, color=(-1, -1, -1), pos=(0, 0))

    elif fixationInfo['targetType'] in ["cross", "line"]:
        fixation = visual.ShapeStim(myWin, lineColor='white',
                                    lineWidth=fixationLineWidth,
                                    vertices=((-fixationSize, 0), (fixationSize, 0),
                                              (0, 0), (0, fixationSize), (0, -fixationSize)),
                                    interpolate=False,
                                    closeShape=False,
                                    pos=(0, 0))

    return fixation


def reportTiming(stimParams):
    """
    Report the timing of the experiment.
    """

    print(f"Experiment timing parameters:")
    print(f"-----------------------------------")
    for (key, value) in stimParams.items():
        print(f"{key}: {value}")
    print(f"-----------------------------------")


def checkForKeyTriggerOrQuit(win, params=None):
    """Check for key trigger or quit.

    Helper function that checks for key presses to either trigger or quit the experiment.
    5, t  -> trigger
    escape, q -> quit

    So you can use this function to quit out of waitForScanner or display loop

    """
    # @todo: add in params for PAUSE_KEY, ALLOW_PAUSE, PAUSE_TIME

    for key in event.getKeys():
        t1 = core.getTime()
        if key in ['5', 't']:
            print(
                "(checkForKeyTriggerOrQuit) got trigger via keyboard -- check that this is what you want...")
            return t1

        elif key in ['escape', 'q']:

            print(
                f"( checkForKeyTriggerOrQuit) user quit via keypress {key}, at time {t1:.3f}s")
            win.close()
            core.quit()

        elif params is not None and params['ALLOW_PAUSE'] and (key in params['PAUSE_KEY']):
            # allow time for a screen shot, eg.
            print(f"Pausing for {params['PAUSE_TIME']} seconds...")
            core.wait(params['PAUSE_TIME'])


def waitForScanner(myWin, fixation=None, params=None, device=None):
    """Wait for the scanner to start.

    waitForScanner(myWin, fixation=None, params=None, device=None):

    """

    assert params is not None, "params dict must be provided"

    # go for digital if USE_VPIXX is true
    method = 'digital' if params['USE_VPIXX'] else 'keyboard'

    # create text stimuli
    message1 = visual.TextStim(myWin, pos=[
                               0, +.5], wrapWidth=1.5, color='#000000', alignText='center', name='topMsg', text="aaa", units='norm')
    message2 = visual.TextStim(myWin, pos=[0, -.5], wrapWidth=1.5, color='#000000',
                               alignText='center', name='bottomMsg', text="bbb", units='norm')

    # wait for scanner
    message1.setText("Please fixate on the central dot during the visual task")
    message2.setText("Press a button when you see a yellow dot at fixation")
    message1.draw()
    message2.draw()
    myWin.flip()

    if method == 'digital':

        myLog = device.din.setDinLog(12e6, 1000)
        device.din.startDinLog()
        device.updateRegisterCache()
        startTime = device.getTime()

        # let's create a loop which checks the schedule for triggers.
        # Any time a trigger is detected, we print the timestamp and DIN state.

        print('(compatibility) waiting for scanner')
        t0 = core.getTime()
        kwait = 1
        while kwait:
            # read device status
            device.updateRegisterCache()
            device.din.getDinLogStatus(myLog)
            newEvents = myLog["newLogFrames"]

            if newEvents > 0:
                t1 = core.getTime()
                eventList = device.din.readDinLog(myLog, newEvents)

                for x in eventList:
                    print(x)
                kwait = 0  # break
                print("-- got trigger via VPIXX!")

            else:
                # but also allow for quitting via keyboard!
                # if we also want to check for trigger, then
                # if this function actually returns, should set
                # kwait = 0
                print(
                    '                you can trigger with t or 5 key, or quit with q/escape')
                t1 = checkForKeyTriggerOrQuit(myWin)
                # kwait = 0

        # Stop logging
        device.din.stopDinLog()
        device.updateRegisterCache()
        return t1, t1-t0

    elif method == 'keyboard' or method == 'manual':
        kwait = 1
        t0 = core.getTime()
        print('(compatibility) waiting for keyboard trigger (debug/scanner emulation)')
        while kwait:
            if fixation is not None:
                fixation.draw()
            myWin.flip()
            t1 = checkForKeyTriggerOrQuit(myWin)
            if t1 is not None:
                kwait = 0

        return t1, t1-t0


# Starting to add in Michaels parallel port output triggers - DM 07/01/2026

def set_all_pins(state, device=None):
    """ Set pins to a specific state.

    Set all pins to the specified state (1 = HIGH, 0 = LOW).
    - state: 1 for HIGH (ON), 0 for LOW (OFF).


    """
    assert device is not None, "Device must be provided as input argument"
    assert state in [0, 1], "State must be 0 (LOW) or 1 (HIGH)"

    myLog = device.din.setDinLog(12e6, 1000)
    device.din.startDinLog()
    device.updateRegisterCache()
    startTime = device.getTime()
    bit_mask = 0xFFFFFF  # Mask for all 24 pins (bits)
    bit_value = 0xFFFFFF if state == 1 else 0x000000  # Set all bits HIGH or LOW
    device.dout.setBitValue(bit_value, bit_mask)
    device.updateRegisterCache()


def set_pin(pin, state, device=None):
    """ Set a specific pin to HIGH or LOW.

    Set a specific pin (bit) to HIGH (1) or LOW (0).
    - pin: The bit position (e.g., 0 for Pin 2, 1 for Pin 3, etc.).
    - state: 1 to turn ON, 0 to turn OFF.
    """

    assert device is not None, "Device must be provided as input argument"
    assert state in [0, 1], "State must be 0 (LOW) or 1 (HIGH)"

    myLog = device.din.setDinLog(12e6, 1000)
    device.din.startDinLog()
    device.updateRegisterCache()
    startTime = device.getTime()
    bit_mask = 1 << pin  # Create a mask for the specific pin
    bit_value = state << pin  # Set the desired state for the specific pin
    device.dout.setBitValue(bit_value, bit_mask)
    device.updateRegisterCache()


def fixationTask(myWin, fixationInfo, params=None, targTime=None, targFlag=None, trialClock=None):
    """
    Function that checks keyboard presses, etc.
    Encapulates the task of checking for key presses and updating the fixation information.
    """

    if params is None:
        BUTTON_CODES = ['1', '2', '3', '4']  # keyboard. fix for VPIXX.
    else:
        BUTTON_CODES = params['BUTTON_CODES']

    # set locally
    nTargsH, nTargsC, nTargsF = 0, 0, 0
    # loop through all keys
    for key in event.getKeys():
        keyTime = trialClock.getTime()
        if key in ['escape', 'q']:
            print(myWin.fps())
            myWin.close()
            core.quit()
        elif key in BUTTON_CODES:
            if targFlag:
                # if there was a target and a response
                # HIT
                if (keyTime-targTime) < 1:  # if within 1s
                    nTargsC = nTargsC+1
                    nTargsH = nTargsH+1
                    targFlag = 0
            else:
                # if there was no target but a response
                # FALSE ALARM
                nTargsC = nTargsC-1
                nTargsF = nTargsF+1

    # store away C, H
    # fixationInfo['nTargs'] += nTargs
    fixationInfo['nTargsH'] += nTargsH
    fixationInfo['nTargsC'] += nTargsC
    fixationInfo['nTargsF'] += nTargsF

    return fixationInfo


def pickFixationColor(fixationInfo, trialClock=None, t_p=None, fixation=None):
    # get a local color_key
    color_key = fixationInfo['color_key']
    fn = fixationInfo['fn']
    my_colors = fixationInfo['my_colors']
    fixLength = fixationInfo['fixLength']
    nTargs = 0
    targFlag = 0
    targTime = 0

    # get the time
    t = trialClock.getTime()
    t_diff = t-t_p
    if t_diff > fixLength:
        old_color_key = color_key
        fnPrev = fn
        while color_key == old_color_key:
            fn = np.random.randint(len(my_colors.keys()))
            color_key = list(my_colors.keys())[fn]
        this_color = my_colors[color_key]
        fixation.setColor(this_color)
        if fn == 3:  # target
            nTargs = nTargs + 1
            targTime = trialClock.getTime()
            targFlag = 1

        t_p = t  # reset the time

    return targTime, targFlag


def showNullPeriod(myWin, fixation, fixationInfo, nullPeriod):
    """
    Show the null period before the experiment starts.
    """
    # loop
    # t = lastFPSupdate = 0
    t_p = 0
    trialClock = core.Clock()

    targFlag = 0
    targTime = 0

    # for the duration of the null period
    while trialClock.getTime() < nullPeriod:

        targTime, targFlag = pickFixationColor(
            fixationInfo, trialClock, t_p, fixation)

        fixation.draw()

        myWin.flip()

        # function that checks keyboard presses, etc.
        fixationInfo = fixationTask(
            myWin, fixationInfo, targTime, targFlag, trialClock)

    return fixationInfo


def endExperiment(myWin):
    """
    End the experiment and show a thank you message.
    """
    # create text stimuli
    message1 = visual.TextStim(myWin, pos=[
                               0, +.5], wrapWidth=1.5, color='#000000', alignText='center', name='topMsg', text="aaa", units='norm')
    message2 = visual.TextStim(myWin, pos=[0, -.5], wrapWidth=1.5, color='#000000',
                               alignText='center', name='bottomMsg', text="bbb", units='norm')

    # show thank you message
    message1.setText("Thank you!")
    message2.setText("Press 'q' or 'escape' to end the session.")
    myWin.clearBuffer()  # clear the screen
    message1.draw()
    message2.draw()
    myWin.flip()
    print("(endExperiment) press 'q' or 'escape' to end the session.")
    thisKey = event.waitKeys(keyList=['q', 'escape'])


def getTimeStr():
    """
    Get the current time as a string.
    """
    return time.strftime("%Y-%m-%dT%H%M%S", time.localtime())


def exportStimulusImage(myWin, params, fileFormat='mat'):
    """
    Export the stimulus as a series of images for pRF analysis.

    NB: currently only supports cw/ccw and exp/con
        and export in .mat format.
    """
    print("(retinotopy) exporting stimulus images...")

    # uses much smaller window (set up after checking args!)
    assert params['TR'] is not None, "TR must be provided as input argument"

    TR = params['TR']
    nFrames = int(params['cycleTime'] / TR * params['nCycles'])
    print(f"(retinotopy) total frames to export for TR {TR}: {nFrames}")

    # make space for export
    imStack = np.empty(np.append(myWin.size, nFrames), dtype=np.float32)

    # create stimulus
    c = np.array((params['centre_x'], params['centre_y']))
    if params['direction'] in ['cw', 'ccw']:
        wedge = SlidingWedge(myWin, pos=c, size=params['size'],
                             dutyCycle=params['dutyCycleWedge'])
    else:
        annulus = SlidingAnnulus(myWin, pos=c, size=params['size'],
                                 dutyCycle=params['dutyCycleRing'])

    for frame in tqdm(range(nFrames)):
        myWin.clearBuffer()
        currentTime = TR*frame

        if params['direction'] in ['cw', 'ccw']:
            # wedge.incrementPhase()
            if params['direction'] == 'cw':
                cycleSpeed = 360.0/params['cycleTime']
            else:
                cycleSpeed = -1.0 * 360.0/params['cycleTime']
            ph = cycleSpeed*currentTime
            wedge.setOri(ph)
            wedge.draw()
        else:
            # annulus.incrementRotation()
            # ph should go from 0 to 1 over cycleTime
            if params['direction'] == 'exp':
                cycleSpeed = -1.0/params['cycleTime']
            else:
                cycleSpeed = 1.0/params['cycleTime']

            ph = cycleSpeed*currentTime % 1.0
            # print(f"cycleSpeed, currentTime, ph: {round(cycleSpeed,2)}, {round(currentTime,2)}, {round(ph ,2)}")
            annulus.setPhase(ph)
            annulus.draw()

        movieFrame = PIL.ImageOps.grayscale(myWin.getMovieFrame(buffer='back'))
        movieFrameNumeric = np.abs(np.array(movieFrame) / 128.0 - 1.0)
        imStack[:, :, frame] = np.transpose(movieFrameNumeric)  # y,x

    # time axis
    t = [f*TR for f in range(nFrames)]
    # x y axes ## need to fix for visual angle size!
    xv, yv = np.meshgrid(np.linspace(-8, 8, myWin.size[0]),
                         np.linspace(-6, 6, myWin.size[1]))
    stim = dict(im=imStack,
                t=t,
                x=xv,
                y=yv)
    fname = f"stim-{params['direction']}-{params['timeStr']}.mat"
    savemat(fname, {'stim': stim})
    print(f"(retinotopy) stimulus export complete: {fname}.")


"""
FlickeringAnnulus not implemented / working yet.
SlidingAnnulus and SlidingWedge are implemented
"""


class FlickeringAnnulus:
    def __init__(self, window,
                 size, pos=[0, 0],
                 dutyCycle=0.25,
                 nRings=4,
                 # duration of full reversal A,B // phase shift per frame (NOT degs, height?)
                 flickerRate=0.1,
                 # (unused?) percentage of frames on which dir changes
                 changeProb=0.01,
                 ):
        self.rings = []
        self.ringWidth = dutyCycle/nRings
        self.flickerRate = flickerRate
        self.changeProb = changeProb
        self.nRings = nRings
        self.pos = pos
        self.size = size
        self.radialPhase = 0
        self._oneCycle = np.arange(0, 1.0, 1/128.0)
        self._oneCycle = np.where(self._oneCycle <= self.ringWidth, 1, 0)
        for n in range(nRings):
            thisStart = self.radialPhase+n*self.ringWidth
            theseIndices = np.arange(thisStart, thisStart+1, 1/128.0) % 1.0
            theseIndices = (theseIndices*128).astype(np.uint8)
            thisMask = self._oneCycle[theseIndices]
            thisRing = visual.RadialStim(window, pos=self.pos,
                                         angularRes=360,
                                         radialCycles=0, angularCycles=16,
                                         size=self.size, texRes=64, mask=thisMask,
                                         )
            self.rings.append(thisRing)

    def draw(self):
        for thisRing in self.rings:
            thisRing.draw()

    def setOri(self, ori):
        for thisRing in self.rings:
            thisRing.setOri(ori)

    def incrementRotation(self):
        if np.random.random() < self.changeProb:
            self.angularRate *= (-1)  # flip the direction by negating the rate
        for n, ring in enumerate(self.rings):  # alternate segments go in and out
            if n % 2 == 0:
                ring.setOri(self.angularRate, '+')
            else:
                ring.setOri(self.angularRate, '-')

    def setPhase(self, phase):
        self.radialPhase = phase
        for n, thisRing in enumerate(self.rings):
            # thisStart = self.radialPhase+n*self.ringWidth
            # theseIndices = np.arange(thisStart, thisStart+1.001, 1/63.0) % 1.0
            # theseIndices = (theseIndices*128).astype(np.uint8)
            # thisMask = self._oneCycle[theseIndices]
            # thisRing.setMask(thisMask)
            thisRing.color = -1*thisRing.color  # toggle the color


class SlidingAnnulus:
    def __init__(self, window,
                 size, pos=[0, 0],
                 dutyCycle=0.25,
                 nRings=4,
                 angularRate=0.1,  # phase shift per frame (NOT degs, height?)
                 changeProb=0.01,  # percentage of frames on which dir changes
                 angularCycles=12):
        self.rings = []
        self.ringWidth = dutyCycle/nRings
        self.angularRate = angularRate
        self.changeProb = changeProb
        self.nRings = nRings
        self.pos = pos
        self.size = size
        self.radialPhase = 0
        self._oneCycle = np.arange(0, 1.0, 1/128.0)
        self._oneCycle = np.where(self._oneCycle <= self.ringWidth, 1, 0)
        for n in range(nRings):
            thisStart = self.radialPhase+n*self.ringWidth
            theseIndices = np.arange(thisStart, thisStart+1, 1/128.0) % 1.0
            theseIndices = (theseIndices*128).astype(np.uint8)
            thisMask = self._oneCycle[theseIndices]
            thisRing = visual.RadialStim(window, pos=self.pos,
                                         angularRes=360,
                                         radialCycles=0, angularCycles=angularCycles,
                                         size=self.size, texRes=64, mask=thisMask,
                                         )
            self.rings.append(thisRing)

    def draw(self):
        for thisRing in self.rings:
            thisRing.draw()

    def setOri(self, ori):
        for thisRing in self.rings:
            thisRing.setOri(ori)

    def incrementRotation(self):
        if np.random.random() < self.changeProb:
            self.angularRate *= (-1)  # flip the direction by negating the rate
        for n, ring in enumerate(self.rings):  # alternate segments go in and out
            if n % 2 == 0:
                ring.setOri(self.angularRate, '+')
            else:
                ring.setOri(self.angularRate, '-')

    def setPhase(self, phase):
        self.radialPhase = phase
        for n, thisRing in enumerate(self.rings):
            thisStart = self.radialPhase+n*self.ringWidth
            theseIndices = np.arange(thisStart, thisStart+1.001, 1/63.0) % 1.0
            theseIndices = (theseIndices*128).astype(np.uint8)
            thisMask = self._oneCycle[theseIndices]
            thisRing.setMask(thisMask)


class SlidingWedge:
    def __init__(self, window, size, pos,
                 dutyCycle=0.125,
                 nSegs=3,
                 # phase shift per frame (fraction of a cycle)
                 radialRate=0.01,
                 changeProb=0.01,  # percentage of frames on which dir changes
                 ):
        self.segments = []
        self.segWidth = dutyCycle*360.0/nSegs
        self.radialRate = radialRate
        self.changeProb = changeProb

        phase = 0
        for n in range(nSegs):
            thisSeg = visual.RadialStim(window, pos=pos, angularRes=360,
                                        radialCycles=6, angularCycles=0,
                                        visibleWedge=[
                                            n*self.segWidth, (n+1)*self.segWidth],
                                        size=size, texRes=64, mask=[1]  # [0.5]
                                        )
            self.segments.append(thisSeg)

    def draw(self):
        for thisSeg in self.segments:
            thisSeg.draw()

    def setOri(self, ori):
        for thisSeg in self.segments:
            thisSeg.setOri(ori)

    def incrementPhase(self):
        if np.random.random() < self.changeProb:
            self.radialRate *= (-1)  # flip the direction by negating the rate
        for n, seg in enumerate(self.segments):  # alternate segments go in and out
            if n % 2 == 0:
                seg.setRadialPhase(self.radialRate, '+')
            else:
                seg.setRadialPhase(self.radialRate, '-')

    def setMask(self, newmask):
        for thisSeg in self.segments:
            thisSeg._set('mask', newmask)


# this is a compatibility layer for the scripts in this folder.
# actually do the version check (if it's being imported)
# can add code in here that will be run if this module is being imported.
# setting defaults, etc.
if __name__ != "__main__":
    versionCheck()
    print("(compatibility) version check.")
else:
    print("(!!) This script is not meant to be run directly. It is a compatibility layer for other scripts.")
    sys.exit(1)
