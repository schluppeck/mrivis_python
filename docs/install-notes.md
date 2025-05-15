# install notes for the 7t set up

On Linux the support for `conda` packages etc not recommeneded[^1]. Decided to go the `pip` route - but keeping versions of python, psychopy etc. the same

```text
python: 3.8.20
# installed version is 3.8.10 -- so should be ok
psychopy version: 2024.2.4
```

Under the `vpixx` login, I follwed these steps to get things up and running.


```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8-venv python3.8-dev
# check that it works as intented

python3.8 -m venv ~/virtualenvs/psychopy  # choose a path of interest!
source ~/virtualenvs/psychopy/bin/activate

# make sure pip is upgraded using the VENV version
sudo /home/vpixx/virtualenvs/psychopy/bin/python -m pip install --upgrade pip

# install wxPython (needed!)
# making sure cpython version 3.8 fits w/ ours
pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/wxPython-4.2.1-cp38-cp38-linux_x86_64.whl

# then pip install psychopy, but pinned to our version
pip install psychopy==2024.2.4

# we also need the vision science plugin
pip install psychopy-visionscience

# and the vpixx linux library
#sudo dpkg -i vpixx-software-tools.deb
# check the downloaded deb file for locations
dpkg -c ~/Downloads/vpixx-software-tools.deb

# usr/local/share/VPixx Software Tools/Software Tools/pypixxlib/pypixxlib-1.6.1.tar.gz
pip install "/usr/local/share/VPixx Software Tools/Software Tools/pypixxlib/pypixxlib-1.6.1.tar.gz"

python ./checkV

```


``bash
#display setup: /home/vpixx/.Psychtoolbox/XorgConfs/90-ptbconfig_2_xscreens_2_outputs_amdgpu.conf
#octave>> XOrgConfSelector
```

## Footnotes


[^1]: https://www.psychopy.org/download.html#conda