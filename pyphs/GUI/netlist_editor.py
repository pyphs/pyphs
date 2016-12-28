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
    QDialog, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from pyphs import PHSNetlist, PHSGraph
from pyphs.graphs.netlists import print_netlist_line
import pyphs.dictionary as PHSdictionary
from importlib import import_module


class NetlistWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):

        # Grid Layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.initMessage()

    def initMessage(self):
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

        labels = ['Dictionary',
                  'Component',
                  'Label',
                  'Nodes',
                  'Arguments']
        data = dict()
        for label in labels:
            data.update({label: list()})

        for netline in self.Netlist:
            for label in labels:
                el = netline[label.lower()]
                el = str(el)[1:-1] if isinstance(el, dict) else str(el)
                data[label] += [el, ]

        # Create Empty (nlines)x5 Table
        table = QTableWidget(self)
        table.setRowCount(self.Netlist.nlines())
        table.setColumnCount(5)

        # Enter data onto Table
        horHeaders = []
        for n, key in enumerate(labels):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                table.setItem(m, n, newitem)

        # Add Header
        table.setHorizontalHeaderLabels(horHeaders)

        # Adjust size of Table
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        # Add Table to Grid
        self.grid.addWidget(table, 0, 0)

    def _new(self):
        fname = QFileDialog.getSaveFileName(self, "New netlist file")[0]
        if not fname[-4:] == '.net':
            fname += '.net'
        self.filename = fname
        print('Netlist filename: ', fname)
        self.Netlist = PHSNetlist(self.filename)
        self._update()

    def _open(self):

        fname = QFileDialog.getOpenFileName(self,
                                            'Open netlist file',
                                            os.getcwd())
        self.filename = fname[0]
        self.Netlist = PHSNetlist(self.filename)
        self._update()

    def _saveas(self):
        fname = QFileDialog.getSaveFileName(self, "Save netlist file as")[0]
        self.Netlist.write(fname)

    def _save(self):
        self.Netlist.write()

    def _plot_graph(self):
        self.Graph = PHSGraph(netlist=self.Netlist)
        self.Graph.plot()


class EditWidget(QWidget):

    def __init__(self, netline=None):
        QWidget.__init__(self)

        self.initUI(netline)

    def initUI(self, netline):

        if netline is None:
            self.netline = {'arguments': {},
                            'component': '',
                            'dictionary': '',
                            'label': '',
                            'nodes': ()}
        else:
            self.netline = netline
        # QLabel
        self.QLabelComponentText = QLabel('', self)
        self.QLabelComponentText.move(10, 10)

        # COMBOS
        self.QComboDictionary = QComboBox(self)
        for dico in PHSdictionary.__all__:
            self.QComboDictionary.addItem(dico)
        self.QComboDictionary.move(0, 20)

        print(bool(len(self.netline['dictionary'])))

        if bool(len(self.netline['dictionary'])):
            self.initQComboComponent()

        self.QComboDictionary.activated[str].connect(self.onActivatedComboDictionary)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Edit component')
        self.show()

    def updateQLabelComponentText(self):
        text = print_netlist_line(self.netline)
        self.QLabelComponentText.setText(text)
        self.QLabelComponentText.adjustSize()

    def onActivatedComboDictionary(self, text):
        self.netline = {'arguments': {},
                        'component': '',
                        'dictionary': text,
                        'label': '',
                        'nodes': ()}
        self.updateQLabelComponentText()
        self.initQComboComponent()

    def initQComboComponent(self):
        print('inside')
        dic = import_module('pyphs.dictionary.' + self.netline['dictionary'])
        self.QComboComponent = QComboBox(self)
        for component in dic.__all__:
            self.QComboComponent.addItem(component)
        self.QComboComponent.activated[str].connect(self.onActivatedComboComponent)
        self.QComboComponent.move(120, 20)

    def onActivatedComboComponent(self, text):
        self.netline.update({'arguments': {},
                             'component': text,
                             'label': '',
                             'nodes': ()})
        self.initUI(self.netline)




class PHSNetlistMainWindow(QMainWindow):

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
        self.openAction.triggered.connect(self.netlist._open)

        # Save Action
        self.saveAction = QAction(QIcon('icons/save.png'), '&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save netlist')
        self.saveAction.triggered.connect(self.netlist._save)

        # Save Action
        self.saveAction = QAction(QIcon('icons/save.png'), '&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save netlist')
        self.saveAction.triggered.connect(self.netlist._save)

        # Saveas Action
        self.saveasAction = QAction(QIcon('icons/saveas.png'),
                                    '&Save as', self)
        self.saveasAction.setShortcut('Ctrl+Shift+S')
        self.saveasAction.setStatusTip('Save as new netlist')
        self.saveasAction.triggered.connect(self.netlist._saveas)

        # PlotGraph Action
        self.plotgraphAction = QAction(QIcon('icons/graph.png'),
                                       '&Plot graph', self)
        self.plotgraphAction.setShortcut('Ctrl+G')
        self.plotgraphAction.setStatusTip('Plot the graph')
        self.plotgraphAction.triggered.connect(self.netlist._plot_graph)

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


def PHSNetlistGUI():
    app = QApplication(sys.argv)
    e = PHSNetlistMainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    e = EditWidget() # PHSNetlistGUI()
    sys.exit(app.exec_())
