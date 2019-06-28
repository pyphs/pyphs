# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:24:12 2016

@author: Falaize
"""

metadata = {'flux': [r'\frac{d\,\phi}{dt}', 'Magnetic flux variation (mfv)', 'V'],
            'effort': [r'\psi', 'Magnetomotive force (mmf)', 'A']}

from ._capacitor import Capacitor
from ._resistor import Resistor
from ._source import Source
from ._capacitorsat import Capacitorsat

__all__ = ['Source', 'Capacitor', 'Resistor', 'Capacitorsat']
