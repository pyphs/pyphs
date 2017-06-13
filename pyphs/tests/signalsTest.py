#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 11:53:37 2017

@author: Falaize
"""

import pyphs.misc.signals as sig
import os
from pyphs import signalgenerator
import numpy as np

here = os.path.realpath(__file__)[:os.path.realpath(__file__).rfind(os.sep)]


def signal_waves():
    """
    Write and read a random sample in wav format
    """
    path = os.path.join(here, 'test.wav')

    s = np.array(list(signalgenerator()()))
    s /= np.max(np.abs(s))

    fs = 1000
    sig.waves.wavwrite(list(s), fs, path, normalize=False, timefades=0.)
    fss, ss = sig.waves.wavread(path)
    os.remove(path)
    ss /= max(abs(ss))
    return max(abs(ss-s)) < 1e-4 and fss - fs < 1e-4


def signal_synthesis():
    sigs = list()
    # test without parameters
    sigs.append(signalgenerator())
    # test for all synthesis methods
    for w in sig.synthesis.names:
        kwargs = {'which': w}
        sigs.append(list(signalgenerator(**kwargs)()))
    return True
