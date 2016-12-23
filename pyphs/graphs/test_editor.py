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
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QFrame, QTextEdit,
    QSplitter, QStyleFactory, QApplication, QAction, QFileDialog, qApp, QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from netlists import Netlist

class NetlistGUI(QTextEdit):
  
    def __init__(self):      
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.data = ""               
                
    def _update(self):
        self.setText(self.data)        
        

    def _new(self):
        dir_ = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        open(dir_, 'a').close()

                
    def _open(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                self.data = f.read()
        self._update()

                
    def _save(self):
        fname = QFileDialog.getSaveFileName(self, "Save file")[0]
        if not fname[-4:] == '.net':
            fname += '.net'
        f = open(fname, 'w')
        f.write(self.data)


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

        # Exit Action
        exitAction = QAction(QIcon('icons/exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(qApp.quit)

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

        #############################################################        

        self.toolbar = self.addToolBar('Tools')
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)

        #############################################################        

        self.statusBar()

        #############################################################        

        menubar = self.menuBar()
        #############################################################
        # Needed on MacOSX only.                                    #
        # This forces in-window menu instead of standard OSX menu   #
        menubar.setNativeMenuBar(False)                             #
        #############################################################        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(exitAction)
        
        #############################################################        

        self.setGeometry(640, 480, 300, 200)
        self.setWindowTitle('PyPHS Editor')    
        self.show()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    e = Editor()
    sys.exit(app.exec_()) 