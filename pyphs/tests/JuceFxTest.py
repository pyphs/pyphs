#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 23:03:18 2018

@author: afalaize
"""
import os
import shutil


def test_method2jucefx():
    from pyphs.examples.bjtamp.bjtamp import core
    from pyphs.misc.juce._fx import method2jucefx

    path = 'temp'

    core.subsinverse()

    method = core.to_method()

    io = (['uIN', ],    # inputs

          ['yOUT', ])   # outputs

    inits = {'u': (0, 0, 9.)}

    method2jucefx(method, path=path, io=io, inits=inits)

    if not os.name.lower().startswith('nt'):
        shutil.rmtree(path)

    return True
