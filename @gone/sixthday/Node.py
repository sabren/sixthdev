"""
Generic class for hierarchical structures.
"""
__ver__="$Id$"

import sixthday
from strongbox import *


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
    parent = link(forward("sixthday.Node"))
    children = linkset(forward("sixthday.Node"), "parent")

    def __init__(self, **kwargs):
        self.private.named = 0
        super(Node, self).__init__(**kwargs)

        
##     def set_path(self, value):
##         # only allow setting once
##         if self.__values__["path"]:
##             raise AttributeError, "Node.path is read only"

    def get_crumbs(self):
        res = []
        node = self
        while node.parent:
            node = node.parent
            res.append( node )
        res.reverse()  # crumbs go top-down, but we went bottom-up :)
        return res
        
##     def set_parent(self, value):
##         assert value is not self, \
##                "A node can't be its own parent!"

    def set_name(self, value):
        self.__values__["name"]=str(value)
        if self.private.named:
            self._updatePath(self.crumbs)
        self.private.named = 1

        
    def _updatePath(self, crumbs):
        path = crumbs + [self]
        self.path = "/".join([n.name for n in path])
        for kid in self.children:
            kid._updatePath(path)

Node.__attrs__["parent"].type=Node
Node.__attrs__["children"].type=Node
