# Vision stimuli for 7T

This repo is a fork of Alex Beckett's https://github.com/AdvancedMRI/python_stimuli code with some modifications to run on later version of PsychoPy. 🙏

2025-05-05, Denis Schluppeck

Stimuli for fMRI experiments written in [PsychoPy](https://www.psychopy.org/download.html)

Stimuli can either be run via command line (my preferred) if PsychoPy module is installed or via the PsychoPy GUI.

Also contains some wrapper shell scripts to run files with specific parameters for previous experiments

- [x] testing compatibility with PsychoPy 2023.2.4
- [ ] adding support for command line argument parsing (`argparse`)
- [ ] setting reasonable default
- [ ] test case `eccLoc.py` for eccentricity version
- [ ] check on fixation task (press on "yellow", data? timings?)
- [ ] adaptation for M/P?
- [ ] pRF stim images saving / computations?

## Notes on installation

If you want to run scripts from the command line, you can try to install dependencies via a `conda` environment.

```bash
# make sure conda is installed.

# add channels
conda config --add channels conda-forge
# create the conda env to make this work...
conda create --name psychopy --file requirements.txt
```

You will also need a local install of `pypixxlib` from VPIXX Technologies. This provides wrappers for the DataPIXX device for button interactions and triggers.

<https://vpixx.com/downloads-and-updates/>

Note: on the Mac, the `pypixxlib` library is located in the following directory:

```bash
# macos 
pypixxpath=/Library/Application\ Support/VPixx\ Technologies/Software\ Tools/pypixxlib/pypixxlib-1.7.0.tar.gz
pip uninstall pypixxlib
pip install $pypixxpath

# make sure you have the psychopy conda env (if local)
python
# >> import pypixxlib
# >> pypixxlib.__file__   # should point to installed file
```

