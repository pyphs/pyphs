#

metadata = {"flux": [r"f", "Not defined", None], "effort": [r"e", "Not defined", None]}

from ._storage import Storage
from ._dissipative import Dissipative
from ._source import Source

__all__ = ["Storage", "Dissipative"]
