
from strongbox import attr, Strongbox, linkset, forward, link
from unittest import TestCase

class Child(Strongbox):
    mama = link(forward)
    name = attr(str)
class Parent(Strongbox):
    kids = linkset(Child, "mama")
Child.__attrs__["mama"].type=Parent

class Node(Strongbox):
    kids = linkset(forward, None)


class NonNode:
    pass

class LinkSetTest(TestCase):

    def test_simple(self):
        p = Parent()
        c = Child(name="freddie jr")
        p.kids << c
        assert p.kids[0] is c
        assert c.mama is p

    def test_typing(self):

        # should not be able to instantiate until we change the "forward" 
        self.assertRaises(ReferenceError, Node)
        Node.__attrs__["kids"].type = Node
        
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
        
