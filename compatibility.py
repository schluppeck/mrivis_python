# compatibility layer
# making sure we have a consistent interface across
# all different scripts in this folder.
#
# this can also contain some site-specific parameters.
#
# 2025-05-05, ds

import psychopy
from psychopy import core, visual, event, gui, plugins

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
        return True
    
    # Check version / deal with stimuli slightly differently
    version = psychopy.__version__

    if str(version) < '2020.1.0':
        print("running an older version of psychopy")
        psychopy_modern = False
    else:   
        print("running somewhere else - modern version of psychopy")
        psychopy_modern = True
        plugins.activatePlugins() # needed for modern version
        visual.PatchStim = visual.GratingStim # PatchStim migrated to GratingStim in newer versions

    return psychopy_modern