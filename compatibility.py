# compatibility layer
# making sure we have a consistent interface across
# all different scripts in this folder.
#
# this can also contain some site-specific parameters.
#
# 2025-05-05, ds

import psychopy
from psychopy import core, visual, event, gui, plugins
import sys
import argparse

# default parameters
SCREEN_SIZE = (1920, 1080)
CHECK_TIMING = False

def versionCheck():
    """
    Check the version of psychopy and return True if it's modern (>= 2020.1.0)
    """
    version = psychopy.__version__
    if str(version) < '2020.1.0':
        print("(compatibility) running an older version of psychopy")
        return False
    else:   
        print(f"\n(compatibility) modern version of psychopy. v{version}")
        psychopy_modern = True
        plugins.activatePlugins() # needed for modern version
        visual.PatchStim = visual.GratingStim # PatchStim migrated to GratingStim in newer version
        return True


def setupParser():
    parser = argparse.ArgumentParser(
        prog = sys.argv[0])
    return parser

def reportTiming(params):
    """
    Report the timing of the experiment.
    """
    onLength = params['onLength']
    offLength = params['offLength']
    numBlocks = params['numBlocks']
    nullPeriod = params['nullPeriod']
    stimSize = params['stimSize']
    flashPeriod = params['flashPeriod']
    
    print(f"on/off: {onLength}/{offLength}")
    print(f"numBlocks: {numBlocks}")
    print(f"nullPeriod: {nullPeriod}")
    print(f"-----------------------------------")
    print(f"TOTAL (s): {(onLength+offLength)*numBlocks + nullPeriod}")
    
def waitForScanner(myWin, fixation):
    """
    Wait for the scanner to start.
    """
    # @TODO make sure it works with VPIXX trigger (not 5!)
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
    t0 = core.getTime()
    while kwait:
        fixation.draw()
        myWin.flip()
        for key in event.getKeys():
            if key in ['5','t']:
                kwait = 0
                t1 = core.getTime()
            elif key in ['escape','q']:
                print(myWin.fps())
                myWin.close()
                core.quit()
    return t1, t1-t0

# this is a compatibility layer for the scripts in this folder.
# actually do the version check (if it's being imported)
# can add code in here that will be run if this module is being imported.
# setting defaults, etc.

if __name__ != "__main__":
    versionCheck()
    print("(compatibility) version check.")
else:
    print("This script is not meant to be run directly. It is a compatibility layer for other scripts.")
    sys.exit(1)
