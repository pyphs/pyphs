#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 19:21:54 2017

@author: Falaize
"""


from ..edges import StorageLinear
from pyphs.config import FS_SYMBS, EPS
from pyphs.core.tools import sympify
from pyphs.dictionary.tools import Argument


class Observerec(StorageLinear):
    """
    Obsevers for an effort and its time integration in one component to plug on
    two nodes (e.g. reference node and mass node to recover the position and
    velocity of the mass).
    """
    def __init__(self, label, nodes):
        """
    Obsevers for an effort and its time integration in one component to plug on
    two nodes (e.g. reference node and mass node to recover the position and
    velocity of the mass).

        Parameters
        ----------

        label : str
            Observer's label. Used to defined the symbols in Core.observers.

        nodes : tuple
            Edge is "nodes[0] -> nodes[1]". This means e.g. in mechanics that
            the velocity associated with nodes[1] is measured relativelty to
            that associated with nodes[0].


        Return
        ------

        obs : Graph
             graph component with one storage edge and two observers:
                * q_label = the storage state x,
                * dtq_label = dx*fs with fs the sample rate.
        """

        # Observer is a stifness with K=0, so that the input is "a" velocity
        # and the responding force is 0. This should not cause any trouble in
        # the solvers, since it is detected as a linear storage component with
        # correponding zero in Q from H(x)=x^T.Q.x, the inverse of which is
        # never computed.
        kwargs = {'name': label,
                  'value': Argument(label + 'coeff', sympify(EPS)),
                  'inv_coeff': False,
                  'ctrl': 'e'}
        StorageLinear.__init__(self, label, nodes, **kwargs)

        # Observer for position q is the state value, which may be initialized.
        q = self.core.symbols('q_'+label)
        q_expr = self.core.x[0]
        obs_q = {q: q_expr}

        # Observer for velocity q is the numerical rate of variation for the
        # position
        dtq = self.core.symbols('dtq_'+label)
        dtq_expr = self.core.dx()[0]*self.core.symbols(FS_SYMBS)
        obs_dtq = {dtq: dtq_expr}

        # update component observers
        self.core.observers.update(obs_q)
        self.core.observers.update(obs_dtq)

    @staticmethod
    def metadata():
        return {'nodes': ('N1', 'N2'),
                'arguments': {}}
