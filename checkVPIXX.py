#! /usr/bin/env python

import psychopy
from psychopy import core, visual, event, gui, plugins
import sys
import argparse
import time
import numpy as np

try:
    from pypixxlib.datapixx import DATAPixx3
    print("(compatibility) using pypixxlib")
except ImportError:
    print("(compatibility) cannot find pypixxlib - UHOH")
    sys.exit(1)

# otherwise we are good to go
try:
    myDevice = DATAPixx3()
except:
    print("No DATAPixx3 found?")
    sys.exit(1012)


# this could fail
myDevice.open()
myDevice.audio.setVolume(0.5)
myDevice.writeRegisterCache()
