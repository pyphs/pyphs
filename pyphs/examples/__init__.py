#

from __future__ import absolute_import

import os
end = os.path.realpath(__file__).rfind(os.sep)
path_to_examples = os.path.realpath(__file__)[:end]

__all__ = ['path_to_examples']
