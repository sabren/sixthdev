"""
The Object Graphics Library provides for simple drawing and manipulation
of 2D objects.
"""

from basic import *
from diagram import *
from canvas import *
from lines import *
from bmpshape import *
from divided import *
from composit import *
from drawn import *


# Set things up for documenting with epydoc.  The __docfilter__ will
# prevent some things from being documented, and anything in __all__
# will appear to actually exist in this module.
import wx._core as _wx
__docfilter__ = _wx.__DocFilter(globals())
__all__ = [name for name in dir() if not name.startswith('_')]

