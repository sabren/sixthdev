
from strongbox import Strongbox, linkset, future
from unittest import TestCase

class Node(Strongbox):
    kids = linkset(future)


class NonNode:
    pass

class LinkSetTest(TestCase):

    def check_typing(self):

        # should not be able to instantiate until we change the "future" 
        self.assertRaises(ReferenceError, Node)
        Node.__attrs__["kids"].setType(Node)

        # now it should work:
        top = Node()
        assert top.kids == [], str(top.kids)

        try:
            top.kids = []
            gotError = 0
        except AttributeError:
            gotError = 1
        assert gotError, "should get error assigning to linkset."

        kidA = Node()
        kidB = Node()

        # I like this syntax better for append...
        top.kids << kidA
        top.kids << kidB
        assert len(top.kids) == 2
        assert top.kids[1] == kidB

        self.assertRaises(TypeError, top.kids.append, NonNode())
        self.assertRaises(TypeError, top.kids.__lshift__, NonNode())
        
