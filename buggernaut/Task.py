"""
Task: stuff to do.
"""
__ver__="$Id$"

from strongbox import *
from pytypes import *
from buggernaut import Area
auto = None

class Task(Strongbox):
    ID = attr(int, default=auto)
    task = attr(str)
    detail = attr(str)
    status = attr(str, default='open',
                  okay=['open', 'urgent', 'active', 'closed'])
    
