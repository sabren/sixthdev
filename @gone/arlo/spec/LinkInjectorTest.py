
from arlo import LinkInjector, MockClerk
from strongbox import Strongbox, attr, link
from unittest import TestCase


class Foreign(Strongbox):
    ID = attr(long)
    data = attr(str)

class InjecteeObj(Strongbox):
    ref = link("Foreign")

class LinkInjectorTest(TestCase):

    def check_inject(self):
        cler = MockClerk()
        cler.store(Foreign(data="Here I come to save the day!"))

        obj = InjecteeObj()
        assert obj.ref is None

        inj = LinkInjector(obj, "ref", cler, Foreign, 1)
        assert len(obj.ref.private.observers) == 1
        
        assert obj.ref is not None, "failed to lazy load."

        # should be able to fetch the ID without triggering load
        assert obj.ref.ID == 1
        assert obj.ref.__values__["data"] == ""
        assert len(obj.ref.private.observers) == 1

        # but getting any other field triggers the load!
        assert obj.ref.data == "Here I come to save the day!"
        assert len(obj.ref.private.observers) == 0
