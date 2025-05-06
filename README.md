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
conda create --name psychopy --file requirements.txt
```