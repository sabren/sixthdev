"""
$Id$
"""

from strongbox import attr, future
#from pytypes import Strict

class TypedList(list):
    
    def __init__(self, classname):
        super(TypedList, self)
        self.settype(classname)

    def settype(self, type):
        self.type = type

    def append(self, value):
        if type(value) == self.type:
            super(TypedList, self).append(value)
        else:
            raise TypeError, "Can't append %s to TypedList(%s)" \
                  % (type(value), self.type)
    
    def __lshift__(self, value):
        self.append(value)


class LinkSet(attr):

    def setType(self, type):
        self.type = type

    def __init__(self, type):
        self.setType(type)

    def initialValue(self):
        if self.type == future:
            raise ReferenceError, \
                  "Can't instantiate -- broken linkset(future) promise."
        else:
            return TypedList(self.type)

    def sanitize(self, value):
        raise AttributeError, "can't assign to linksets (only append/delete)"

