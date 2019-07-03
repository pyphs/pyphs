#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:12:19 2017

@author: Falaize
"""
from pyphs import Graph
from ..connectors import Gyrator
from ..magnetics import Source, Capacitor
from ..edges import Observerec
from ..tools import mappars
from ..tools import componentDoc, parametersDefault
from ..transducers import metadata as dicmetadata


class Pickup(Graph):

    def __init__(self, label, nodes, **kwargs):

        Graph.__init__(self, label=label)

        parameters = parametersDefault(self.metadata['parameters'])
        parameters.update(kwargs)

        Ccoil = float(parameters.pop('Ccoil'))
        Ncoil = float(parameters.pop('Ncoil'))

        # remove H0
        parameters.pop('H0')
        dicpars, subs = mappars(self, **parameters)

        # parameters
        pars = ['Rb', 'Rp', 'Lh', 'Lv']
        Rb, Rp, Lh, Lv = self.core.symbols(pars)

        # nodes
        MASS, ELEC1, ELEC2 = nodes
        NMagnet = 'N' + label + 'Magnet'
        NCcoil = 'N' + label + 'Ccoil'

        self += Source(label+'Magnet',
                       (self.datum, NMagnet),
                       **{'type': 'mmf'})

        MASS_obs = Observerec(label+'OBS', (self.datum, MASS))
        self += MASS_obs
        q, dtq = MASS_obs.core.o()

        def f(q, dtq):
            """
            cf JSV Rhodes eq (25)
            set dmu = (murel-1)/(murel + 1) to 1
            """
            dmu = 1
            f1 = (q - Rp + Lv)**2 + Lh**2
            f2 = (q + Rp + Lv)**2 + Lh**2
            return 2*Rb**2*dmu*Rp*((f1-2*Lh**2)/f1**2 -
                                   (f2-2*Lh**2)/f2**2) * dtq

        falpha = (f(q, dtq)**-1).subs(dicpars)
        self += Gyrator(label+'MecToMag',
                        (self.datum, NCcoil, self.datum, NMagnet),
                        alpha=(label+'f', falpha))
        self += Capacitor(label+'Ccoil',
                          (self.datum, NCcoil),
                          C=Ccoil)
        self += Gyrator(label+'MagToElec',
                        (self.datum, NCcoil, ELEC1, ELEC2),
                        alpha=(label+'Ncoil', Ncoil))
        self.core.subs.update(subs)

    metadata = {'title': 'Electro-magnetic Pickup',
                'component': 'Pickup',
                'label': 'pick',
                'dico': 'transducers',
                'desc': 'Electro-magnetic pickup as found in electric instruments (guitars and piano). See [1]_ for details.',
                'nodesdesc': "MEC is a mechanical node. EL1, EL2 are electrical nodes with positive output current EL1->EL2.",
                'nodes': ('MEC', 'EL1', 'EL2'),
                'parametersdesc': 'Component parameter.',
                'parameters': [['Lv', "Vertical distance", 'm', 1e-3],
                               ['Lh', "Horizontal distance", 'm', 5e-4],
                               ['Ccoil', "Pickup coil inductance", 'W/K2', 3e-5],
                               ['Ncoil', "Number of pickup coil wire turns", 'd.u.', 1e2],
                               ['Rb', "Moving ball radius", 'm', 1e-3],
                               ['Rp', "Pickup coil radius", 'm', 1e-3],
                               ['H0', "Constant mmf of pickup magnet", 'A', 1.]],
                'refs': {1: 'Antoine Falaize and Thomas Helie. Passive simulation of the nonlinear port-hamiltonian modeling of a rhodes piano. Journal of Sound and Vibration, 2016.'},
                'nnodes': 6,
                'nedges': 7,
                'flux': dicmetadata['flux'],
                'effort': dicmetadata['effort'],
                }

    __doc__ = componentDoc(metadata)
