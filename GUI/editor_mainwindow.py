#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows
how to use QSplitter widget.

author: Jan Bodnar
website: zetcode.com
last edited: January 2015
"""

from __future__ import absolute_import, division, print_function

from PyQt5.QtWidgets import (QAction, qApp, QMainWindow)
from PyQt5.QtGui import QIcon

from netlistwidget import NetlistWidget
from netlistwidget.base import iconspath


class NetlistEditor(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.initUI()

    def initUI(self):

        self.netlist = NetlistWidget()
        self.setCentralWidget(self.netlist)

        #############################################################
        #############################################################
        #############################################################

        # Main Actions

        # Exit Action
        exitAction = QAction(QIcon(iconspath + 'exit.png'),
                             '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(qApp.quit)

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

        self.toolbarNetlist = self.addToolBar('Netlist')
        self.toolbarNetlist.addAction(self.netlist.newAction)
        self.toolbarNetlist.addAction(self.netlist.openAction)
        self.toolbarNetlist.addAction(self.netlist.saveAction)
        self.toolbarNetlist.addAction(self.netlist.saveasAction)
        self.toolbarNetlist.addAction(self.netlist.addlineAction)
        self.toolbarNetlist.addAction(self.netlist.editAction)
        self.toolbarNetlist.addAction(self.netlist.plotgraphAction)

        #############################################################
        #############################################################
        #############################################################

        # Status Bar

        self.statusBar()

        #############################################################
        #############################################################
        #############################################################

        # MENU BAR

        menubar = self.menuBar()
        #############################################################
        # Needed on MacOSX only.                                    #
        # This forces in-window menu instead of standard OSX menu   #
        menubar.setNativeMenuBar(False)                             #
        #############################################################

        # PyPHS menu
        fileMenu = menubar.addMenu('&Netlist')
        fileMenu.addAction(self.netlist.newAction)
        fileMenu.addAction(self.netlist.openAction)
        fileMenu.addAction(self.netlist.saveAction)
        fileMenu.addAction(self.netlist.saveasAction)
        fileMenu.addAction(exitAction)

        # Netlist menu
        netlistMenu = menubar.addMenu('&Line')
        netlistMenu.addAction(self.netlist.addlineAction)
        netlistMenu.addAction(self.netlist.editAction)

        # Plots menu
        plotsMenu = menubar.addMenu('&Plots')
        plotsMenu.addAction(self.netlist.plotgraphAction)

        #############################################################

        self.resize(640, 300)
        self.setWindowTitle('PyPHS Editor')
        self.show()
