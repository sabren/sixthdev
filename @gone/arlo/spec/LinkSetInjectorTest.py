
from storage import MockStorage
from arlo import LinkSetInjector, Clerk
from strongbox import Strongbox, attr, linkset, forward
from unittest import TestCase


class Content(Strongbox):
    ID = attr(long)
    box = attr(forward)
    data = attr(str)

class Package(Strongbox):
    ID = attr(long)
    refs = linkset(Content, None)

Content.__attrs__["box"].type=Package

class LinkSetInjectorTest(TestCase):

    def check_inject(self):

        ms = MockStorage()
        ms.store("Package")
        ms.store("Content", data="I'm content", boxID=1)
        ms.store("Content", data="I'm mal content", boxID=1)
        
        clerk = Clerk(ms, {})
        clerk.dbmap[Package.__attrs__["refs"]]=(Content, "boxID")
        assert type(Package.__attrs__["refs"]) != attr

        pak = Package()
        pak.refs << Content(data="I'm content", box=pak)
        pak.refs << Content(data="I'm malcontent",  box=pak)
        pak = clerk.store(pak)

        pak = clerk.fetch(Package, ID=1)
        
        # @TODO: should be able to add to the index without triggering load
        # (for performance reasons)

        # asking for .refs will trigger the load:
        assert len(pak.private.refs) == 0
        assert len(pak.refs) == 2

        # make sure it works with << on a fresh load too:
        newClerk = Clerk(ms, clerk.dbmap)
        newClerk.storage = clerk.storage
        pak = newClerk.fetch(Package, ID=1)
        assert len(pak.private.refs) == 0
        pak.refs << Content(data="I'm malcontent",  box=pak)
        assert len(pak.refs) == 3
