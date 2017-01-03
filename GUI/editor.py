#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 14:52:19 2017

@author: Falaize
"""
from __future__ import absolute_import


from editor_mainwindow import NetlistEditor, QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = NetlistEditor()
    sys.exit(app.exec_())
