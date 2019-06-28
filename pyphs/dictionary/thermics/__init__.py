#

metadata = {'desc': 'This dictionary contains elementary thermal components.',
            'effort': [r'\theta', 'Temperature', 'K'],
            'flux': [r'\frac{d\sigma}{dt}', 'Entropy variation', 'W/K']}

from ._capacitor import Capacitor
from ._transfers import Transfer
from ._source import Source

__all__ = ['Capacitor', 'Transfer', 'Source']
