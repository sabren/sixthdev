
from arlo import LinkSetInjector, MockClerk
from strongbox import Strongbox, attr, linkset
from unittest import TestCase


class Foreign(Strongbox):
    ID = attr(long)
    injID = attr(long)
    data = attr(str)

class InjecteeObj(Strongbox):
    ID = attr(long)
    refs = linkset(Foreign)

class LinkSetInjectorTest(TestCase):

    def check_inject(self):
        cler = MockClerk()
        cler.store(Foreign(data="Here I come to save the day!", injID=1))
        cler.store(Foreign(data="Mighty Mouse is on his way!",  injID=1))

        obj = InjecteeObj()
        assert type(obj.__attrs__["refs"]) != attr
        cler.store(obj)

        inj = LinkSetInjector(obj, "refs", cler, Foreign, "injID")
        assert len(obj.private.observers) == 1

        obj.refs << Foreign(data="Faster than a speeding bullet!")

        # @TODO: should be able to add to the index without triggering load
        # (for performance reasons)
        #assert len(obj.__values__["refs"]) == 1

        # but getting any other field triggers the load!
        assert obj.refs[0].data == "Here I come to save the day!"
        assert len(obj.private.observers) == 0

        assert len(obj.refs) == 3
        
