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
    QDialog, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QComboBox,
    QLineEdit, QDialogButtonBox, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from pyphs import PHSNetlist, PHSGraph
from pyphs.graphs.netlists import print_netlist_line
import pyphs.dictionary as PHSdictionary
from importlib import import_module
import ast
from PyQt5 import QtCore

iconspath = './icons' + os.sep


class NetlistWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.initUI()

    def initUI(self):

        # Grid Layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.initMessage()

        self.resize(self.sizeHint())


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

    def _new_line(self):
        netline = {'arguments': {},
                   'component': '',
                   'dictionary': '',
                   'label': '',
                   'nodes': ()}
        self.Netlist.add_line(netline)
        self._update()
        self._edit_line(i=self.Netlist.nlines()-1)

    def _edit_line(self, i=None):
        if i is None:
            text, ok = QInputDialog.getText(self,
                                            'Edit netlist line',
                                            'Select a line number (int):'
                                            )
            if ok:
                i = int(text)-1
                line = self.Netlist[i]
                netline, res = EditDialog.getNetline(self, line)
                self.Netlist.setline(i, netline)
                self._update()
        else:
            line = self.Netlist[i]
            netline, res = EditDialog.getNetline(self, line)
            self.Netlist.setline(i, netline)
            self._update()


###############################################################################

class EditDialog(QDialog):

    def __init__(self, parent=None, netline=None):
        super(EditDialog, self).__init__(parent)
        self.ypos = 0
        self.ypostext = 50
        self.initUI(netline)

    def initUI(self, netline):

        self.grid = QGridLayout()

        if netline is None:
            self.netline = {'arguments': {},
                            'component': '',
                            'dictionary': '',
                            'label': '',
                            'nodes': ()}
        else:
            self.netline = netline

        self.label = QLineEdit(self)
        self.label.setText(self.netline['label'])
#        self.label.move(0, self.ypos)
        self.label.textChanged[str].connect(self.onChanged_label)

        # QLabel
        self.Qlabel = QLabel('', self)
#        self.Qlabel.move(0, self.ypostext)

        self.init_dico()

        vbox = QVBoxLayout()
        vbox.addWidget(self.Qlabel)
        vbox.addLayout(self.grid)
        vbox.addStretch(1)
        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        vbox.addWidget(buttons)

        self.setLayout(vbox)

        self.setWindowTitle('Edit component')
        self.show()

    def onChanged_label(self, text):
        self.netline['label'] = str(text)
        self.update_Qlabel()

    def update_Qlabel(self):
        text = print_netlist_line(self.netline)
        self.Qlabel.setText(text)
        self.Qlabel.adjustSize()

    def update_grid(self):
        self.grid.addWidget(QLabel('Label'), 0, 0)
        self.grid.addWidget(QLabel('Dictionary'), 0, 1)
        self.grid.addWidget(QLabel('Component'), 0, 2)
        self.grid.addWidget(QLabel('Nodes'), 0, 3)
        self.grid.addWidget(QLabel('Parameters'), 0, 4)
        append = False
        if hasattr(self, 'Qcomp'):
            try:
                w = self.grid.itemAtPosition(1, 2).widget()
                w.setParent(None)
                self.grid.removeWidget(w)
            except AttributeError:
                pass
            if self.Qcomp is not None:
                self.grid.addWidget(self.Qcomp, 1, 2)
                append = True
        if not append:
            b = QLineEdit(self)
            self.grid.addWidget(b, 1, 2)
        append = False
        if hasattr(self, 'nodes'):
            try:
                w = self.grid.itemAtPosition(1, 3).widget()
                w.setParent(None)
                self.grid.removeWidget(w)
            except AttributeError:
                pass

            for i, n in enumerate(self.nodes):
                if n is not None:
                    position = (i+1, 3)
                    self.grid.addWidget(n, *position)
                    append = True
        if not append:
            b = QLineEdit(self)
            self.grid.addWidget(b, 1, 3)

        append = False
        if hasattr(self, 'arguments'):
            try:
                w = self.grid.itemAtPosition(1, 4).widget()
                w.setParent(None)
                self.grid.removeWidget(w)
            except AttributeError:
                pass
            for i, a in enumerate(self.arguments):
                if a is not None:
                    self.grid.addWidget(a, i+1, 4)
                    append = True
        if not append:
            b = QLineEdit(self)
            self.grid.addWidget(b, 1, 4)

    ###########################################################################
    # COMBOS
    def init_dico(self):
        self.Qdico = QComboBox(self)
        self.grid.addWidget(self.label, 1, 0)
        self.grid.addWidget(self.Qdico, 1, 1)
        self.Qdico.addItem('Select...')
        for dico in PHSdictionary.__all__:
            self.Qdico.addItem(dico)

        index = self.Qdico.findText(self.netline['dictionary'],
                                    QtCore.Qt.MatchFixedString)
        self.Qdico.activated[str].connect(self.onActivated_Qdico)

        if index >= 0:
            self.Qdico.setCurrentIndex(index)
        self.init_comp()

    def onActivated_Qdico(self, text):
        self.netline.update({'arguments': {},
                             'component': '',
                             'dictionary': str(text),
                             'nodes': ()})
        self.clean_comp()
        self.update_Qlabel()
        if str(text) == 'Select...':
            pass
        else:
            self.init_comp()

    ###########################################################################

    def clean_comp(self):
        try:
            self.grid.removeWidget(self.Qcomp)
        except  AttributeError:
                pass
        try:
            if self.Qcomp is not None:
                self.Qcomp.deleteLater()
                self.Qcomp = None
        except  AttributeError:
                pass
        self.clean_pars()

    def init_comp(self):
        self.Qcomp = QComboBox(self)
        self.Qcomp.show()
        try:
            dic = import_module('.'+self.netline['.dictionary'], 'PHSdictionary')
            for _ in range(self.Qcomp.count()):
                self.Qcomp.removeItem(0)
            self.Qcomp.addItem('Select...')
            for component in dic.__all__:
                self.Qcomp.addItem(component)
            self.Qcomp.activated[str].connect(self.onActivated_Qcomp)
            index = self.Qcomp.findText(self.netline['component'],
                                        QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.Qcomp.setCurrentIndex(index)
        except (ValueError, KeyError):
            pass
        self.init_parameters()

    def onActivated_Qcomp(self, text):
        self.netline.update({'arguments': {},
                             'component': str(text).lower(),
                             'nodes': ()})
        self.clean_pars()
        self.update_Qlabel()
        if str(text) == 'Select...':
            pass
        else:
            self.init_parameters()

    ###########################################################################

    def clean_pars(self):
        try:
            for i, node in enumerate(self.nodes):
                    self.grid.removeWidget(node)
                    node.deleteLater()
                    self.nodes[i] = None
        except AttributeError:
            pass
        try:
            for i, arg in enumerate(self.arguments):
                self.grid.removeWidget(arg)
                arg.deleteLater()
                self.arguments[i] = None
        except AttributeError:
            pass

    def init_parameters(self):
        try:
            dic = import_module('.'+self.netline['dictionary'],
                                'PHSdictionary')
            comp = getattr(dic,
                           self.netline['component'][0].upper() +
                           self.netline['component'][1:])
            if self.netline['nodes'] == ():
                nodes = comp.metadata()['nodes']
                self.netline['nodes'] = nodes
            else:
                nodes = self.netline['nodes']
            if len(self.netline['arguments']) == 0:
                arguments = comp.metadata()['arguments']
                self.netline['arguments'] = arguments
            else:
                arguments = self.netline['arguments']

            def widget_generator(label):
                class mywidget(QWidget):
                    def __init__(self):
                        QWidget.__init__(self)
                        hbox = QHBoxLayout()
                        hbox.addWidget(QLabel(str(label) + ':'))
                        self.qle = QLineEdit(self)
                        hbox.addWidget(self.qle)
                        self.setLayout(hbox)
                return mywidget

            def onchange_generator(target, index):

                def onchange_node(text):
                    tup = self.netline['nodes']
                    lis = list(tup)
                    lis[index] = str(text)
                    self.netline['nodes'] = tuple(lis)
                    self.update_Qlabel()

                def onchange_arg(text):
                    try:
                        value = ast.literal_eval(text)
                    except (ValueError, SyntaxError):
                        value = str(text)
                    self.netline['arguments'][index] = value
                    self.update_Qlabel()

                if target == 'nodes':
                    return onchange_node
                elif target == 'arguments':
                    return onchange_arg

            self.nodes = []
            for i, node in enumerate(nodes):
                self.nodes.append(widget_generator(comp.metadata()['nodes'][i])())
                onchange = onchange_generator('nodes', i)
                self.nodes[-1].qle.textChanged[str].connect(onchange)
                self.nodes[-1].qle.setText(node)
                self.nodes[-1].show()

            self.arguments = []
            for i, arg in enumerate(arguments.keys()):
                w = widget_generator(comp.metadata()['arguments'].keys()[i])()
                self.arguments.append(w)
                onchange = onchange_generator('arguments', arg)
                self.arguments[-1].qle.textChanged[str].connect(onchange)
                obj = arguments[arg]
                if isinstance(obj, str):
                    self.arguments[-1].qle.setText("'%s'" % obj)
                else:
                    self.arguments[-1].qle.setText(str(obj))
                self.arguments[-1].show()
        except (KeyError, IndexError, ValueError):
            pass
        self.update_Qlabel()
        self.update_grid()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getNetline(parent=None, netline=None):
        dialog = EditDialog(parent, netline)
        result = dialog.exec_()
        netline = dialog.netline
        return (netline, result == QDialog.Accepted)


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
        exitAction = QAction(QIcon(iconspath + 'exit.png'),
                             '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit PyPHS Editor')
        exitAction.triggered.connect(qApp.quit)

        #############################################################
        #############################################################
        #############################################################

        # Netlist Actions

        # Open Action
        self.openAction = QAction(QIcon(iconspath + 'open.png'),
                                  '&Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open netlist')
        self.openAction.triggered.connect(self.netlist._open)

        # Save Action
        self.saveAction = QAction(QIcon(iconspath + 'icons/save.png'),
                                  '&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save netlist')
        self.saveAction.triggered.connect(self.netlist._save)

        # Save Action
        self.saveAction = QAction(QIcon(iconspath + 'save.png'),
                                  '&Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save netlist')
        self.saveAction.triggered.connect(self.netlist._save)

        # Saveas Action
        self.saveasAction = QAction(QIcon(iconspath + 'saveas.png'),
                                    '&Save as', self)
        self.saveasAction.setShortcut('Ctrl+Shift+S')
        self.saveasAction.setStatusTip('Save as new netlist')
        self.saveasAction.triggered.connect(self.netlist._saveas)

        # Edit Action
        self.editAction = QAction(QIcon(iconspath + 'edit.png'),
                                  '&Edit', self)
        self.editAction.setShortcut('Ctrl+E')
        self.editAction.setStatusTip('Edit netlist line')
        self.editAction.triggered.connect(self.netlist._edit_line)

        # PlotGraph Action
        self.plotgraphAction = QAction(QIcon(iconspath + 'graph.png'),
                                       '&Plot graph', self)
        self.plotgraphAction.setShortcut('Ctrl+G')
        self.plotgraphAction.setStatusTip('Plot the graph')
        self.plotgraphAction.triggered.connect(self.netlist._plot_graph)

        # addline Action
        self.addlineAction = QAction(QIcon(iconspath + 'add.png'),
                                     '&Add a new line', self)
        self.addlineAction.setShortcut('Ctrl+L')
        self.addlineAction.setStatusTip('Add a new line to the netlist')
        self.addlineAction.triggered.connect(self.netlist._new_line)

        #############################################################
        #############################################################
        #############################################################

        # TOOLBAR

        self.toolbarNetlist = self.addToolBar('Netlist')
        self.toolbarNetlist.addAction(self.openAction)
        self.toolbarNetlist.addAction(self.saveAction)
        self.toolbarNetlist.addAction(self.saveasAction)
        self.toolbarNetlist.addAction(self.addlineAction)
        self.toolbarNetlist.addAction(self.editAction)
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
        fileMenu = menubar.addMenu('&Netlist')
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveasAction)
        fileMenu.addAction(exitAction)

        # Netlist menu
        netlistMenu = menubar.addMenu('&Line')
        netlistMenu.addAction(self.addlineAction)
        netlistMenu.addAction(self.editAction)

        # Plots menu
        plotsMenu = menubar.addMenu('&Plots')
        plotsMenu.addAction(self.plotgraphAction)

        #############################################################

        self.resize(640, 300)
        self.setWindowTitle('PyPHS Editor')
        self.show()


def PHSNetlistGUI():
    app = QApplication(sys.argv)
    e = PHSNetlistMainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    PHSNetlistGUI()