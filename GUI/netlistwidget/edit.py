#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 12:03:33 2017

@author: Falaize
"""

from __future__ import absolute_import, division, print_function

import sys

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout,
                             QApplication, QDialog, QLabel, QGridLayout,
                             QComboBox, QLineEdit, QDialogButtonBox)
from PyQt5.QtCore import Qt

from pyphs.graphs.netlists import print_netlist_line
import pyphs.dictionary as PHSdictionary
import ast

###############################################################################


class LabelWidget(QLineEdit):
    def __init__(self, label=None):
        QLineEdit.__init__(self)
        if label is None:
            label = ""
        self.setText(label)

###############################################################################


class EditDialog(QDialog):

    def __init__(self, parent=None, netline=None):
        super(EditDialog, self).__init__(parent)

        self.initUI(netline)

    def initUI(self, netline):

        self.grid = QGridLayout()
        self.grid.addWidget(QLabel('Label'), 0, 0)
        self.grid.addWidget(QLabel('Dictionary'), 0, 1)
        self.grid.addWidget(QLabel('Component'), 0, 2)
        self.grid.addWidget(QLabel('Nodes'), 0, 3)
        self.grid.addWidget(QLabel('Parameters'), 0, 4)

        if netline is None:
            netline = {'arguments': None,
                       'component': None,
                       'dictionary': None,
                       'label': None,
                       'nodes': None}
        self.netline = netline

        self.label = LabelWidget(self.netline['label'])

        self.netlistQlabel = QLabel('', self)

        self.Qdico = QComboBox(self)
        self.grid.addWidget(self.label, 1, 0)
        self.grid.addWidget(self.Qdico, 1, 1)
        self.Qdico.addItem('Select...')
        for dico in PHSdictionary.__all__:
            self.Qdico.addItem(dico)

        self.label.textChanged[str].connect(self.onChanged_label)
        self.Qdico.activated[str].connect(self.onActivated_dico)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        index = self.Qdico.findText(self.netline['dictionary'],
                                    Qt.MatchFixedString)
        if index >= 0:
            self.Qdico.setCurrentIndex(index)

        self.init_comp()
        vbox = QVBoxLayout()
        vbox.addWidget(self.netlistQlabel)
        vbox.addLayout(self.grid)
        vbox.addStretch(1)
        vbox.addWidget(buttons)
        self.setLayout(vbox)
        self.setWindowTitle('Edit component')
        self.show()

    def onChanged_label(self, text):
        self.netline['label'] = str(text)
        self.update_Qlabel()

    def update_Qlabel(self):
        text = print_netlist_line(self.netline)
        self.netlistQlabel.setText(text)
        self.netlistQlabel.adjustSize()

    def update_grid(self):

        item = self.grid.itemAtPosition(1, 2)
        if item is not None:
            w = item.widget()
            w.setParent(None)
            self.grid.removeWidget(w)
        self.grid.addWidget(self.Qcomp, 1, 2)

        item = self.grid.itemAtPosition(1, 3)
        if item is not None:
            w = item.widget()
            w.setParent(None)
            self.grid.removeWidget(w)
        for i, n in enumerate(self.nodes):
            position = (i+1, 3)
            self.grid.addWidget(n, *position)

        item = self.grid.itemAtPosition(1, 4)
        if item is not None:
            w = item.widget()
            w.setParent(None)
            self.grid.removeWidget(w)
        for i, a in enumerate(self.arguments):
            if a is not None:
                self.grid.addWidget(a, i+1, 4)

    ###########################################################################
    def onActivated_dico(self, text):
        self.netline.update({'dictionary': str(text),
                             'arguments': None,
                             'component': None,
                             'nodes': None})
        self.update_Qlabel()
        if str(text) == 'Select...':
            pass
        else:
            self.init_comp()

    ###########################################################################

    def init_comp(self):
        if self.netline['dictionary'] is None:
            self.Qcomp = QLineEdit(self)
        else:

            self.Qcomp = QComboBox(self)
            self.Qcomp.activated[str].connect(self.onActivated_Qcomp)
            dic = getattr(PHSdictionary, self.netline['dictionary'])
            self.Qcomp.addItem('Select...')
            for component in dic.__all__:
                self.Qcomp.addItem(component)

            index = self.Qcomp.findText(self.netline['component'],
                                        Qt.MatchFixedString)
            if index >= 0:
                self.Qcomp.setCurrentIndex(index)
        self.init_parameters()

    def onActivated_Qcomp(self, text):
        self.netline.update({'component': str(text).lower(),
                             'arguments': None,
                             'nodes': None})
        self.clean_pars()
        self.update_Qlabel()
        if str(text) == 'Select...':
            pass
        else:
            self.init_parameters()

    ###########################################################################

    def clean_pars(self):
        for i, node in enumerate(self.nodes):
                self.grid.removeWidget(node)
                node.deleteLater()
                self.nodes[i] = None
        for i, arg in enumerate(self.arguments):
            self.grid.removeWidget(arg)
            arg.deleteLater()
            self.arguments[i] = None

    def init_parameters(self):

        self.nodes = []
        self.arguments = []

        if self.netline['component'] is None:
            self.nodes.append(QLineEdit(self))
            self.arguments.append(QLineEdit(self))
        else:
            dic = getattr(PHSdictionary, self.netline['dictionary'])
            comp = getattr(dic,
                           self.netline['component'][0].upper() +
                           self.netline['component'][1:])
            if self.netline['nodes'] is None:
                nodes = comp.metadata()['nodes']
                self.netline['nodes'] = nodes
            else:
                nodes = self.netline['nodes']
            if self.netline['arguments'] is None:
                arguments = comp.metadata()['arguments']
                self.netline['arguments'] = arguments
            else:
                arguments = self.netline['arguments']

            for i, node in enumerate(nodes):
                w = self.widget_generator(comp.metadata()['nodes'][i])()
                self.nodes.append(w)
                onchange = self.onchange_generator('nodes', i)
                self.nodes[-1].qle.textChanged[str].connect(onchange)
                self.nodes[-1].qle.setText(node)
                self.nodes[-1].show()

            for i, arg in enumerate(arguments.keys()):
                label = list(comp.metadata()['arguments'].keys())[i]
                w = self.widget_generator(label)()
                self.arguments.append(w)
                onchange = self.onchange_generator('arguments', arg)
                self.arguments[-1].qle.textChanged[str].connect(onchange)
                obj = arguments[arg]
                if isinstance(obj, str):
                    self.arguments[-1].qle.setText("'%s'" % obj)
                else:
                    self.arguments[-1].qle.setText(str(obj))
                self.arguments[-1].show()
        self.update_Qlabel()
        self.update_grid()

    def widget_generator(self, label):
        class MyWidget(QWidget):
            def __init__(self):
                QWidget.__init__(self)
                hbox = QHBoxLayout()
                hbox.addWidget(QLabel(str(label) + ':'))
                self.qle = QLineEdit(self)
                hbox.addWidget(self.qle)
                self.setLayout(hbox)
        return MyWidget

    def onchange_generator(self, target, index):

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

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getNetline(parent=None, netline=None):
        dialog = EditDialog(parent, netline)
        result = dialog.exec_()
        netline = dialog.netline
        return (netline, result == QDialog.Accepted)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    e = EditDialog()
    sys.exit(app.exec_())
