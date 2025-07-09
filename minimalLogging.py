#! /usr/bin/env python

# -*- coding: utf-8 -*-
"""
Minimal logging example for keeping track of events / data

Uses python's built-in logging module to log events rather than psychopy - to 
make formatting of log entries a bit more flexible.

ds 2025-06-23

"""

from psychopy import core

# provide a compatibility layer for newer versions of PsychoPy
# and some site-specific parameters
from compatibility import getTimeStr

# not psychopy, but handrolled?
import logging


def setupLogging(name=__name__, level=logging.INFO):
    """
    Set up the logging configuration for the script.
    This function configures the logging to write to a file with a timestamp.
    """
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # get current time as string for log file name
    ts = getTimeStr()
    logfileName = f"log-{ts}.txt"

    # configure logging to write to a file
    logging.basicConfig(filename=logfileName,
                        format='%(asctime)s;%(levelname)s;%(message)s',
                        level=logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s;%(name)s;%(levelname)s;%(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    # also append warnings to a central log file
    ts = getTimeStr()

    logger = setupLogging(name=__name__, level=logging.DEBUG)
    logfileName = f"_trial-log-{ts}.txt"

    logging.basicConfig(filename=logfileName,
                        format='%(asctime)s;%(levelname)s;%(message)s',
                        level=logging.DEBUG)

    print("Welcome to the logging example!")
    print(f"test started: {ts}")
    print(f"logging to {logfileName}")

    trialClock = core.Clock()
    t0 = trialClock.getTime()
    nTrials = 10
    for i in range(nTrials):
        t1 = trialClock.getTime() - t0
        # message comma separated, so that it can be read by a spreadsheet
        logging.info(f"{t1};trial {i+1}/{nTrials}")
        core.wait(1.5)

    print("done with local timing testing...")
