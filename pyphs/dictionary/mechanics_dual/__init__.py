#
metadata = {'desc': 'This dictionary contains elementary mechanical components.',
            'effort': [r'f', 'Force', 'N'],
            'flux': [r'v', 'Velocity', 'm/s']}

from ._mass import Mass
from ._stiffness import Stiffness
from ._damper import Damper
from ._source import Source
from ._springsat import Springsat
from ._springcubic import Springcubic
from ._felt import Felt


__all__ = ['Source', 'Stiffness', 'Mass', 'Damper',
           'Springcubic', 'Springsat', 'Felt']
