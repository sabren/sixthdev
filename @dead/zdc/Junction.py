"""
Junction - *:* relationships
"""
__ver__="$Id$"

import zdc

class Junction(zdc.LinkSet):
    __super = zdc.LinkSet
    """
    This does the grunt work for working with
    foreign keys in a *:* relationship.

    @TODO: clarify this documentation.. it even confuses me.
    lKey is local (or left hand) key fieldname (ON THE FOREIGN TABLE!)
    rKey is remote (or right-hand) key fieldname
    lID is the actual value for the local key
    """
    __super = zdc.LinkSet

    def __init__(self, owner, rClass, table=None, lKey=None, rKey=None):
        self.__super.__init__(self, owner, rClass, lKey, rKey)
        self.table = table

    def load(self):
        pass

    def save(self):
        pass
