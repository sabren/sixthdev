
from arlo import LinkInjector, Schema, MockClerk
from strongbox import *
from unittest import TestCase

class Foreign(Strongbox):
    ID = attr(long)
    data = attr(str)

class Local(Strongbox):
    ref = link(Foreign)


class LinkInjectorTest(TestCase):

    def check_inject(self):
        """
        basic test case.
        """
        schema = Schema({
            Foreign: "foregin",
            Local: "local",
            Local.ref: "foreignID",
        })
        clerk = MockClerk(schema)
        
        obj = Local()
        assert obj.ref is None

        clerk.store(Foreign(data="Here I come to save the day!"))

        obj.ref = Foreign(ID=1)
        obj.ref.addInjector(LinkInjector(clerk, Foreign, 1).inject)
        assert len(obj.ref.private.injectors) == 1

        # should be able to fetch the ID without triggering load
        assert obj.ref.ID == 1
        assert obj.ref.private.data == ""
        assert len(obj.ref.private.injectors) == 1

        # but getting any other field triggers the load!
        assert obj.ref.data == "Here I come to save the day!"
        assert len(obj.ref.private.injectors) == 0


    def check_with_linkset(self):
        """
        what happens if the thing we're injecting
        has a linkset of its own (this used to fail)
        """

        class Kid(Strongbox):
            ID = attr(long)
            parent = link(forward)
        
        class Parent(Strongbox):
            ID = attr(long)
            name = attr(str)
            kids = linkset(Kid, "parent")
            
        Kid.parent.type = Parent
        
        class Uncle(Strongbox):
            brother = link(Parent)

        schema = Schema({
            Kid: "kid",
            Kid.parent: "parentID",
            Parent: "parent",
            Uncle: "uncle",
            Uncle.brother: "brotherID",
        })
        clerk = MockClerk(schema)


        kid = Kid()
        dad = Parent(name="Brother Dad")
        dad.kids << kid
        clerk.store(dad)
        
        unc = Uncle()
        unc.brother = Parent(ID=1)
        unc.brother.addInjector(LinkInjector(clerk, Parent, 1).inject)

        ## this next line threw an AttributeError because the
        ## injector tried to include "kids" in the .update() call
        assert unc.brother.name=="Brother Dad"
        
