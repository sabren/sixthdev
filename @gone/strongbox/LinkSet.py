"""
$Id$
"""

from strongbox import attr, forward
#from pytypes import Strict

class TypedList(list):
    
    def __init__(self, klass, owner, backlink):
        super(TypedList, self)
        self.setType(klass)
        self.backlink = backlink
        self.owner = owner

    def setType(self, type):
        self.type = type

    def append(self, other):
        if type(other) == self.type:
            super(TypedList, self).append(other)
        else:
            raise TypeError, "Can't append %s to TypedList(%s)" \
                  % (type(other), self.type)
        if self.backlink is not None:
            setattr(other, self.backlink, self.owner)
    
    def __lshift__(self, other):
        self.append(other)
        return other

class LinkSet(attr):

    def __init__(self, type, back):
        """
        type: the type of objects in the collection
        back: the name of the backlink in the child (can be None)

        For example, parent.children might have a backlink of
        child.parent so you'd say:

        class Parent(Strongbox):
            children = linkset(Child, 'parent')
        
        """
        self.type = type
        self.back = back      

    def initialValue(self, instance):
        if self.type == forward:
            raise ReferenceError, \
                  "Can't instantiate -- broken linkset(forward) promise."
        else:
            return TypedList(self.type, instance, self.back)

    def sanitize(self, other):
        raise AttributeError, "can't assign to linksets (only append/delete)"

