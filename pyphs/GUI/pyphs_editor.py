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

import sys
import os
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame,
    QSplitter, QStyleFactory, QApplication, QAction, QFileDialog, qApp,
    QPushButton, QMainWindow, QTextEdit, QDesktopWidget, QMessageBox,
    QDialog, QLabel, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from netlist_editor import NetlistWidget


class Splitter(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):

        #############################################################

        hbox = QHBoxLayout(self)

        #############################################################

        self.netlist = NetlistWidget()

        topright = QFrame(self)
        topright.setFrameShape(QFrame.StyledPanel)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        #############################################################

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.netlist)
        splitter1.addWidget(topright)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

class Editor(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.initUI()

    def initUI(self):

        self.splitter = Splitter()
        self.setCentralWidget(self.splitter)

        #############################################################
        #############################################################
        #############################################################

        # Main Actions

        # Exit Action
        exitAction = QAction(QIcon('icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(qApp.quit)

        #############################################################
        #############################################################
        #############################################################

        # Netlist Actions

        # Open Action
        self.openAction = QAction(QIcon('icons/open.png'), '&Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open netlist')
        self.openAction.triggered.connect(self.splitter.netlist._open)

        # Save Action
        self.saveAction = QAction(QIcon('icons/save.png'), '&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save netlist')
        self.saveAction.triggered.connect(self.splitter.netlist._save)

        # Save Action
        self.saveAction = QAction(QIcon('icons/save.png'), '&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save netlist')
        self.saveAction.triggered.connect(self.splitter.netlist._save)

        # Saveas Action
        self.saveasAction = QAction(QIcon('icons/saveas.png'),
                                    '&Save as', self)
        self.saveasAction.setShortcut('Ctrl+Shift+S')
        self.saveasAction.setStatusTip('Save as new netlist')
        self.saveasAction.triggered.connect(self.splitter.netlist._saveas)

        # PlotGraph Action
        self.plotgraphAction = QAction(QIcon('icons/graph.png'),
                                       '&Plot graph', self)
        self.plotgraphAction.setShortcut('Ctrl+G')
        self.plotgraphAction.setStatusTip('Plot the graph')
        self.plotgraphAction.triggered.connect(self.splitter.netlist._plot_graph)

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

        self.toolbarNetlist = self.addToolBar('Netlist')
        self.toolbarNetlist.addAction(self.openAction)
        self.toolbarNetlist.addAction(self.saveAction)
        self.toolbarNetlist.addAction(self.saveasAction)
        self.toolbarNetlist.addAction(self.plotgraphAction)

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
        fileMenu = menubar.addMenu('&PyPHS')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(exitAction)

        # Netlist menu
        netlistMenu = menubar.addMenu('&Netlist')
        netlistMenu.addAction(self.openAction)
        netlistMenu.addAction(self.saveAction)
        netlistMenu.addAction(self.saveasAction)
        netlistMenu.addAction(self.plotgraphAction)

        #############################################################

        self.setGeometry(640, 480, 300, 200)
        self.setWindowTitle('PyPHS Editor')
        self.showMaximized()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    e = Editor()
    sys.exit(app.exec_())