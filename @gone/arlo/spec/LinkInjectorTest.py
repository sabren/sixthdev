
from arlo import LinkInjector, MockClerk
from strongbox import *
from unittest import TestCase

class Foreign(Strongbox):
    ID = attr(long)
    data = attr(str)

class Local(Strongbox):
    ref = link(Foreign)


class LinkInjectorTest(TestCase):

    def setUp(self):
        self.clerk = MockClerk()
        
    def check_inject(self):
        """
        basic test case.
        """
        obj = Local()
        assert obj.ref is None

        self.clerk.store(Foreign(data="Here I come to save the day!"))

        obj.ref = Foreign(ID=1)
        obj.ref.attach(LinkInjector(self.clerk, Foreign, 1), onget="inject")
        assert len(obj.ref.private.observers) == 1

        # should be able to fetch the ID without triggering load
        assert obj.ref.ID == 1
        assert obj.ref.__values__["data"] == ""
        assert len(obj.ref.private.observers) == 1

        # but getting any other field triggers the load!
        assert obj.ref.data == "Here I come to save the day!"
        assert len(obj.ref.private.observers) == 0

    def check_with_linkset(self):
        """
        what happens if the thing we're injecting
        has a linkset of its own (this used to fail)
        """                       
        class Parent(Strongbox):
            ID = attr(long)
            name = attr(str)
            kids = linkset(Foreign)
            
        class Uncle(Strongbox):
            brother = link(Parent)

        self.clerk.dbmap[Parent.__attrs__["kids"]] = (Foreign, "parentID")

        kid = Foreign(data="i'm a toys r us kid!")
        dad = Parent(name="Brother Dad")
        dad.kids << kid
        self.clerk.store(dad)
        
        unc = Uncle()
        unc.brother = Parent(ID=1)
        unc.brother.attach(LinkInjector(self.clerk, Parent, 1),
                           onget="inject")

        ## this next line threw an AttributeError because the
        ## injector tried to include "kids" in the .update() call
        assert unc.brother.name=="Brother Dad"
        
