"""
Type labels..
"""
__ver__="$Id$"

from strongbox import *

class Type(Strongbox):
    ID = attr(int)
    label = attr(str)
