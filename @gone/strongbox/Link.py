"""
$Id$
"""

import strongbox
from strongbox import attr

class Link(attr):
    """
    Represents a one-way link to another Strongbox.
    """

    def __init__(self, classname):
        self.type = classname
        self.default = None
        self.okay = None


    def _typeok(self, value):
        return isinstance(value, strongbox.Strongbox) \
               and value.__class__.__name__==self.type
    
