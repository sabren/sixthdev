"""
$Id$
"""

import strongbox
from strongbox import attr

class Link(attr):
    """
    Represents a one-way link to another Strongbox.
    """
    def __init__(self, klass):
        self.type = klass
        self.default = None
        self.okay = None
        self.allowNone = 1

    def _typeok(self, value):
        return isinstance(value, self.type)    
