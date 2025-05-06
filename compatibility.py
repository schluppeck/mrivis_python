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
        print("running an older version of psychopy")
        return False
    else:   
        print("running somewhere else - modern version of psychopy")
        psychopy_modern = True
        plugins.activatePlugins() # needed for modern version
        visual.PatchStim = visual.GratingStim # PatchStim migrated to GratingStim in newer version
        return True


def setupParser():
    parser = argparse.ArgumentParser(
        prog = sys.argv[0])
    return parser

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
