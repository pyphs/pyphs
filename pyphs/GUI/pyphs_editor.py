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

import sys
import os
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, 
    QSplitter, QStyleFactory, QApplication, QAction, QFileDialog, qApp, 
    QPushButton, QMainWindow, QTextEdit, QDesktopWidget, QMessageBox, 
    QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon 

from pyphs import PHSNetlist


class NetlistGUI(QTextEdit):
  
    def __init__(self):      
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        msgBox = QMessageBox()
        msgBox.setText('Netlist file selection')
        msgBox.addButton(QPushButton('New'), QMessageBox.YesRole)
        msgBox.addButton(QPushButton('Open'), QMessageBox.NoRole)
        init = msgBox.exec_()
        
        if init == 0:
            self._new()
        else:
            assert init == 1
            self._open()

    def _update(self):
        self.setText(self.Netlist.netlist())        
        
    def _new(self):
        fname = QFileDialog.getSaveFileName(self, "New netlist file")[0]
        if not fname[-4:] == '.net':
            fname += '.net'
        self.filename = fname
        print('Netlist filename: ', fname)
        self.Netlist = PHSNetlist(self.filename)
        self._update()
                
    def _open(self):

        fname = QFileDialog.getOpenFileName(self, 'Open netlist file', os.getcwd())
        self.filename = fname[0]
        self.Netlist = PHSNetlist(self.filename)
        self._update()
                
    def _saveas(self):
        fname = QFileDialog.getSaveFileName(self, "Save netlist file as")[0]
        self.Netlist.write(fname)

    def _save(self):
        self.Netlist.write()

class Splitter(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        #############################################################        

        hbox = QHBoxLayout(self)

        #############################################################        

        self.netlist = NetlistGUI()
        self.netlist.setFrameShape(QFrame.StyledPanel)
 
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
                
    def onChanged(self, text):
        
        self.lbl.setText(text)
        self.lbl.adjustSize()        

class Editor(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
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
        self.saveasAction = QAction(QIcon('icons/saveas.png'), '&Save as', self)        
        self.saveasAction.setShortcut('Ctrl+Shift+S')
        self.saveasAction.setStatusTip('Save as new netlist')
        self.saveasAction.triggered.connect(self.splitter.netlist._saveas)

        #############################################################        
        #############################################################        
        #############################################################        
        
        # TOOLBAR

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

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

        #############################################################        

        self.setGeometry(640, 480, 300, 200)
        self.setWindowTitle('PyPHS Editor')    
        self.show()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    e = Editor()
    sys.exit(app.exec_()) 