#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:12:19 2017

@author: Falaize
"""
from pyphs import PHSGraph
from ..connectors import Gyrator
from ..mechanics import Stiffness
from ..magnetics import Source, Capacitor
from ..edges import Observerabs
from ..tools import mappars
__all__ = ['Pickup']


def parameters_JSV2016():
    pars = { 
            # Inductance of the pickup [Henries] 
            'Ccoil':3.30*1e-5, 
            # Nb of pickup coil wire turns
            'Ncoil':100.,
            # Magnetic material radius
            'Rb':1e-3,
            # Pickup coil radius
            'Rp':1e-3,
            # Magnetomotive force of the magnet
            'H0':-1.,
            # [m] horizontal position of the pick-up w.r.t the beam at rest
            'Lh': 1.5*1e-3, 
            # [m] vertical position of the pick-up w.r.t the beam at rest
            'Lv': 5e-4, 
    }

    return pars

    
class Pickup(PHSGraph):
    """
======
Pickup
======
Electro-mecanique Pickup as found in electric instruments (guitars and piano)

Parameters
-----------

label: str
    Pickup label.

nodes : (MEC, N1, N2)
    Nodes for connection    
    * MEC is a mechanical node,
    * EL1, EL2 are electrical nodes.

kwargs : dictionary with following "key: value" (default in parenthesis)
    * 'Ccoil': [H] Pickup coil inductance (3.3*1e-5),
    * 'Ncoil': [d.u] Number of pickup coil wire turns (1e2),
    * 'Rb': [m] Moving ball radius (1e-3),
    * 'Rp': [m] pickup coil radius (1e-3),
    * 'H0': [A] Constant magnetomotive force of pickup magnet (1.),
    * 'Lv': [m] Vertical distance (1.5*1e-3),
    * 'Lh': [m] Horizontal distance (5e-4),
    """
    def __init__(self, label, nodes, **kwargs):

        PHSGraph.__init__(self, label=label)

        pars = parameters_JSV2016()
        pars.update(kwargs)
        Ccoil = pars.pop('Ccoil')
        Ncoil = pars.pop('Ncoil')
        dicpars, subs = mappars(self, **pars)
        print(dicpars)
        print(subs)
        self.core.subs.update(subs)
        # parameters
        pars = ['Rb', 'Rp', 'H0', 'Lh', 'Lv']
        Rb, Rp, H0, Lh, Lv = self.core.symbols(pars)

        MECA, ELEC1, ELEC2 = nodes
        
        
        observer = Observerabs(label+'obs', (MECA, ))
        self += observer

        q = observer.core.x[0]
        dtq = observer.core.w[0]

        NMagnet = 'N' + label + 'Magnet'
        NCcoil = 'N' + label + 'Ccoil'

        self += Source(label+'Magnet',
                       (self.datum, NMagnet),
                       **{'type': 'mmf'},
                       const=pars['H0'])
        def f(q, dtq):
            """
            cf JSV Rhodes eq (25)
            set dmu = (murel-1)/(murel + 1) to 1
            """
            dmu = 1
            f1 = (q - Rp + Lv)**2 + Lh**2
            f2 = (q + Rp + Lv)**2 + Lh**2
            return 2*Rb**2*dmu*Rp*((f1-2*Lh**2)/f1**2 - (f2-2*Lh**2)/f2**2)*dtq
        falpha = f(q, dtq).subs(dicpars)
        print('falpha: {}'.format(falpha))
        self += Gyrator(label+'MecToMag',
                        (self.datum, NMagnet, self.datum, NCcoil),
                        alpha=(label+'f', falpha))
        self += Capacitor(label+'Ccoil',
                          (self.datum, NCcoil),
                          C=Ccoil)
        self += Gyrator(label+'MagToElec',
                        (self.datum, NCcoil, ELEC1, ELEC2),
                        alpha=(label+'Ncoil', Ncoil))
    @staticmethod
    def metadata():
        return {'nodes': ('MECA', 'ELEC1', 'ELEC2'),
                'arguments': {'Lp':330*1e-9,
                              'Ncoil':100.,
                              'murel':700.,
                              'Rb':1e-3,
                              'Rp':1e-3,
                              'H0':-1.,
                              'Lh':1.5*1e-3, 
                              'Lv':5e-4,}
                              }
                              