"""
Goals to be achieved.
"""
__ver__="$Id$"

from strongbox import *

class Goal(Strongbox):
    name = attr(str)
    description = attr(str)
