#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:44:58 2017

@author: Falaize
"""


class CanNotUnlock(Exception):
    pass


class UndefinedPotential(Exception):
    pass


class FluxCtrlIsEffortCtrl(Exception):
    pass


class EffortCtrlIsFluxCtrl(Exception):
    pass
