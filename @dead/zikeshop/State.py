"""
zikeshop.State - states, with sales tax info
"""
__ver__="$Id$"
from strongbox import *
from pytypes import FixedPoint

class State(Strongbox):
    code = attr(str)
    salestax = attr(FixedPoint)

