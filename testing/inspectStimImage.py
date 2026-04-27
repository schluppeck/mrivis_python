#!/usr/bin/env python

# visualise pRF stim images...

from matplotlib import pyplot as plt
from scipy.io import savemat, loadmat
from psychopy import core, gui
from psychopy import __version__ as PSYCHOPY_VERSION
import skimage.util
import sys
import os
import argparse
import numpy as np


def setupParser(description="Display and debug stim images..."):
    parser = argparse.ArgumentParser(
        prog=sys.argv[0])

    parser.description = description
    parser.add_argument('--filename', dest='filename',
                        type=str) # not required, but pop gui if not given
    parser.add_argument('--info', dest='INFO', action='store_true',
                        help='show some diagnostic info about the stim image')
    parser.add_argument('--montage', dest='MONTAGE',
                        action='store_true', help='show stim image montage')

    return parser

parser = setupParser()

args = parser.parse_args().__dict__.copy()

if args['filename'] is None:
    # pop a gui to get the filename
    fileDlg = gui.fileOpenDlg(prompt='Select a .mat file containing the stim image',    
                             allowed='*.mat')
    if fileDlg is not None:
        args['filename'] = fileDlg[0]
        # and decide default behaviour
        args['INFO'] = True
        args['MONTAGE'] = True
    else:
        print('No file selected, exiting...')
        core.quit()

# load data file straight into memory
D = loadmat(args['filename'])

if args['INFO']:
    print('stim image shape: {}'.format(D['stim']['im'].item().shape))
    print('stim image max: {}'.format(D['stim']['im'].item().max()))
    print('stim image min: {}'.format(D['stim']['im'].item().min()))

if args['MONTAGE']:
    # show a montage of the stim images
    # (planes, rows, columns)
    theImage = np.transpose(D['stim']['im'].item(), (2, 1, 0))  # t, x, y
    M = skimage.util.montage(theImage, 
                             padding_width = 2,
                             fill=1)
    print(f"{M.shape}")
    plt.imshow(M, aspect='equal', cmap='gray')
    plt.title(
        f"Montage from {os.path.basename(args['filename'])}\nrows, then columns")
    plt.tight_layout()
    plt.axis('off')
    plt.show()
