
from storage import MockStorage
from arlo import LinkSetInjector, Clerk, Schema
from strongbox import *
from unittest import TestCase


class Content(Strongbox):
    ID = attr(long)
    box = link(forward)
    data = attr(str)

class Package(Strongbox):
    ID = attr(long)
    refs = linkset(Content, "box")

Content.box.type=Package

class LinkSetInjectorTest(TestCase):

    def check_inject(self):

        ms = MockStorage()
        ms.store("Package")
        ms.store("Content", data="I'm content", boxID=1)
        ms.store("Content", data="I'm mal content", boxID=1)

        schema = Schema({
            Content: "content",
            Content.box: "boxID",
            Package: "package",
        })

        clerk = Clerk(ms, schema)

        pak = Package()
        pak.refs << Content(data="I'm content", box=pak)
        pak.refs << Content(data="I'm malcontent", box=pak)
        pak = clerk.store(pak)

        # @TODO: should be able to add to the index without
        # triggering load (for performance reasons)
        # -- so long as any other use DOES trigger load --


        clerk.cache.clear()
        pak = clerk.fetch(Package, ID=1)
        
        # asking for .refs will trigger the load:
        assert len(pak.private.refs) == 0, pak.private.refs
        assert len(pak.refs) == 2

        # make sure it works with << on a fresh load too:
        newClerk = Clerk(clerk.storage, clerk.schema)
        pak = newClerk.fetch(Package, ID=1)
        assert len(pak.private.refs) == 0
        pak.refs << Content(data="I'm malcontent",  box=pak)
        assert len(pak.refs) == 3
