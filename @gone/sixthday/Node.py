"""
Generic class for hierarchical structures.
"""
__ver__="$Id$"

import zdc
import sixthday
from strongbox import Strongbox, attr, link, future


##----------------------------------------------
## [0528.2002 01:32]
## This code is probably good, but not working yet.
## we can't do this without the ability to do recursive links.
##----------------------------------------------

class Node(Strongbox):

    ID = attr(long)
    name = attr(str)
    path = attr(str)
    note = attr(str)

    def set_path(self, value):
        # only allow setting once
        if self.__values__["path"]:
            raise AttributeError, "Node.path is read only"

    def get_crumbs(self):
        res = []
        node = self
        raise "@TODO: can't use crumbs until 'parent' works"
        while node.parent:
            node = node.parent
            res.append( node )
        res.reverse()  # crumbs go top-down, but we went bottom-up :)
        return res
        
##     def set_parent(self, value):
##         assert value is not self, \
##                "A node can't be its own parent!"

##     def _updatePaths(self, parent=None):
##         # this is a recursive version.. It's probably really slow.
        
##         if parent:
##             self._data["path"] = parent.path + "/" + self.name
##         else:
##             self._data["path"] = self.name

##         super(Node,self).save()
        
##         for kid in self.q_children():
##             child = Node(self._ds, ID=kid["ID"])
##             child._updatePaths(parent=self)
##             child.save()  
