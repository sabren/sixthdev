"""
$Id$
"""

from strongbox import attr, forward
#from pytypes import Strict

class TypedList(list):
    
    def __init__(self, klass):
        super(TypedList, self)
        self.setType(klass)

    def setType(self, type):
        self.type = type

    def append(self, value):
        if type(value) == self.type:
            super(TypedList, self).append(value)
        else:
            raise TypeError, "Can't append %s to TypedList(%s)" \
                  % (type(value), self.type)
    
    def __lshift__(self, value):
        self.append(value)
        return value

class LinkSet(attr):

    def __init__(self, type):
        self.type = type

    def initialValue(self):
        if self.type == forward:
            raise ReferenceError, \
                  "Can't instantiate -- broken linkset(forward) promise."
        else:
            return TypedList(self.type)

    def sanitize(self, value):
        raise AttributeError, "can't assign to linksets (only append/delete)"

