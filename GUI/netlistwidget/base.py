#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 11:54:56 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sys
import os
from PyQt5.QtWidgets import (QWidget, QAction,
                             QApplication, QFileDialog,
                             QPushButton, QMessageBox,
                             QTableWidget, QTableWidgetItem, QInputDialog,
                             QGridLayout, QAbstractItemView)
from PyQt5.QtGui import QIcon
from pyphs import PHSNetlist, PHSGraph
from .edit import EditDialog

iconspath = '.' + os.sep + 'icons' + os.sep


class NetlistWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('PyPHS Editor')
        self.initUI()

    def initUI(self):

        # Create Empty (nlines)x5 Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.labels = ('Dictionary', 'Component', 'Label',
                       'Nodes', 'Arguments')

        # Add Header
        horHeaders = []
        for n, key in enumerate(self.labels):
            horHeaders.append(key)
        self.table.setHorizontalHeaderLabels(horHeaders)

        # set Layout
        self.grid = QGridLayout()
        self.grid.addWidget(self.table, 0, 0)
        self.setLayout(self.grid)

        # Netlist Actions

        # New Action
        self.newAction = QAction(QIcon(iconspath + 'new.png'),
                                 '&New Netlist', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('Create a new netlist')
        self.newAction.triggered.connect(self._new)

        # Open Action
        self.openAction = QAction(QIcon(iconspath + 'open.png'),
                                  '&Open Netlist', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open an existing netlist')
        self.openAction.triggered.connect(self._open)

        # Save Action
        self.saveAction = QAction(QIcon(iconspath + 'save.png'),
                                  '&Save Netlist', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save the netlist')
        self.saveAction.triggered.connect(self._save)

        # Saveas Action
        self.saveasAction = QAction(QIcon(iconspath + 'saveas.png'),
                                    '&Save Netlist as', self)
        self.saveasAction.setShortcut('Ctrl+Shift+S')
        self.saveasAction.setStatusTip('Save as a new netlist')
        self.saveasAction.triggered.connect(self._saveas)

        # Edit Action
        self.editAction = QAction(QIcon(iconspath + 'edit.png'),
                                  '&Edit line', self)
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit an existing line of the netlist')
        self.editAction.triggered.connect(self._edit_line)

        # PlotGraph Action
        self.plotgraphAction = QAction(QIcon(iconspath + 'graph.png'),
                                       '&Plot graph', self)
        self.plotgraphAction.setShortcut('Ctrl+G')
        self.plotgraphAction.setStatusTip('Plot the graph')
        self.plotgraphAction.triggered.connect(self._plot_graph)

        # addline Action
        self.addlineAction = QAction(QIcon(iconspath + 'add.png'),
                                     '&New line', self)
        self.addlineAction.setShortcut('Ctrl+L')
        self.addlineAction.setStatusTip('Add a new line to the netlist')
        self.addlineAction.triggered.connect(self._new_line)

        self.initMessage()

        self.resize(self.table.sizeHint())
        self.show()

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

    def update(self):

        # get data
        data = dict()
        for label in self.labels:
            data.update({label: list()})
        for netline in self.Netlist:
            for label in self.labels:
                el = netline[label.lower()]
                if isinstance(el, dict):
                    string = ''
                    for k in el.keys():
                        string += "{0!s}: {1!s}; ".format(k, el[k])
                    string = string[:-1]
                elif isinstance(el, tuple):
                    string = ''
                    for obj in el:
                        string += "{0!s}, ".format(obj)
                    string = string[:-1]
                else:
                    string = str(el)
                data[label].append(string)

        # Enter data onto Table
        self.table.setRowCount(self.Netlist.nlines())
        for n, key in enumerate(self.labels):
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.table.setItem(m, n, newitem)

        # Adjust size of Table
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def _new(self):
        fname = QFileDialog.getSaveFileName(self, "New netlist file")[0]
        if not fname[-4:] == '.net':
            fname += '.net'
        self.filename = fname
        print('Netlist filename: ', fname)
        self.Netlist = PHSNetlist(self.filename)
        self.update()

    def _open(self):

        fname = QFileDialog.getOpenFileName(self,
                                            'Open netlist file',
                                            os.getcwd())
        self.filename = fname[0]
        self.Netlist = PHSNetlist(self.filename)
        self.update()

    def _saveas(self):
        fname = QFileDialog.getSaveFileName(self, "Save netlist file as")[0]
        if not fname == '':
            self.Netlist.write(fname)

    def _save(self):
        self.Netlist.write()

    def _plot_graph(self):
        self.Graph = PHSGraph(netlist=self.Netlist)
        self.Graph.plot()

    def _new_line(self):
        netline, res = EditDialog.getNetline(self)
        if res:
            self.Netlist.add_line(netline)
            self.update()

    def _edit_line(self):
        text, ok = QInputDialog.getText(self,
                                        'Edit netlist line',
                                        'Select a line number (int):'
                                        )
        if bool(ok):
            i = int(text)-1
            line = self.Netlist[i]
            netline, res = EditDialog.getNetline(self, line)
            if res:
                self.Netlist.setline(i, netline)
                self.update()


###############################################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = NetlistWidget()
    sys.exit(app.exec_())
