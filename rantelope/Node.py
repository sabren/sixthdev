"""
A really kludgy base class for trees.

It sucks because it's tightly coupled
with the database.

On the other hand, it hides all the
nasty stuff so you can just subclass
it. The only requirements are that you
assign .clerk before traversing the
tree.

Remember to redefine  ID and parentID 
in your subclass - strongbox doesn't
yet let you inherit attrs.
"""
__ver__="$Id$"
from strongbox import *

class Node(Strongbox):
    ID = attr(long)
    parentID = attr(int)

    def __init__(self, clerk=None, **kwargs):
        super(Node, self).__init__(**kwargs)
        if clerk:
            self.private.clerk = clerk

    def get_crumbs(self):
        res = []
        node = self
        while node.parent:
            node = node.parent
            res.append( node )
        res.reverse()
        return res

    def set_clerk(self, clerk):
        self.private.clerk = clerk


    ### @TODO: have addto_XXXs() encapsulate << on linksets
    def add(self, kid):
        assert isinstance(kid, self.__class__), \
               "child must be a %s" % self.__class__.__name__
        if not self.ID:
            # what a horrible kludge this is:
            newme = self.private.clerk.store(self)
            self.ID = newme.ID
        kid.parentID = self.ID
        kid.clerk = self.private.clerk
        self.private.clerk.store(kid)

    def get_kids(self):
        self.__ensureclerk()
        res = self.private.clerk.match(self.__class__, parentID=self.ID)
        for n in res:
            n.clerk = self.private.clerk
        return res
            
    def get_parent(self):
        self.__ensureclerk()
        if self.parentID:
            res = self.private.clerk.fetch(self.__class__, self.parentID)
            res.clerk = self.private.clerk
            return res
        else:
            return None

    def __ensureclerk(self):
        if not hasattr(self.private, "clerk"):
            raise AssertionError, "cannot traverse tree without a clerk"


if __name__=="__main__":

    ## Demo code for working with Nodes
    ## @TODO: Make this a pyunit TestCase.
    
    import arlo, sqlRantelope, storage

    class TestNode(Node):
        ID = attr(long)
        parentID = attr(int)
        name = attr(str)
        note = attr(str)
    
    dbmap = { TestNode: "rnt_node" }
    clerk = arlo.Clerk(storage.MySQLStorage(sqlRantelope.dbc), dbmap)

    for x in clerk.match(TestNode):
        clerk.delete(TestNode, x.ID)

    n = TestNode(clerk=clerk, name='n1')
    n.add(TestNode(name="n2"))

    print n
    print n.kids
