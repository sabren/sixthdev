"""
Generic class for hierarchical structures.
"""
__ver__="$Id$"

import sixthday
from strongbox import *

class Node(Strongbox):
    ID = attr(long)
    name = attr(str)
    path = attr(str)
    data = attr(str)
    parent = link(forward("sixthday.Node"))
    children = linkset(forward("sixthday.Node"), "parent")

    def __init__(self, **kwargs):
        super(Node, self).__init__()
        self.private.named = False
        self.update(**kwargs)
       
##     def set_path(self, value):
##         # only allow setting once
##         if self.private.path:
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
        self.private.name=str(value)
        # this .private.named thing prevents a max
        # bug of some kind. It probably needs a
        # closer look.
        if self.private.named:
            self._updatePath(self.crumbs)
        self.private.named = True

        
    def _updatePath(self, crumbs):
        path = crumbs + [self]
        self.path = "/".join([n.name for n in path])
        for kid in self.children:
            kid._updatePath(path)

Node.parent.type=Node
Node.children.type=Node
