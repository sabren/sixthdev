
from arlo import Clerk
from storage import MockStorage
from strongbox import Strongbox, attr, link, linkset, forward
import unittest

class Record(Strongbox):
    ID = attr(long)
    val = attr(str)
    next = link(forward)
Record.__attrs__["next"].type=Record

class Node(Strongbox):
    ID = attr(long)
    data = attr(str)
    parentID = attr(long)
    kids = linkset(forward)
Node.__attrs__["kids"].type=Node   


class ClerkTest(unittest.TestCase):

    def setUp(self):
        self.storage = MockStorage()
        self.clerk = Clerk(self.storage)
        # @TODO: figure out how to let me use Record.next here..
        self.clerk.dbmap[Record.__attrs__["next"]] = (Record, 'nextID')
        self.clerk.dbmap[Node.__attrs__["kids"]] = (Node, 'parentID')


    def check_store(self):
        """
        When we store a record, the attrs get
        stored but the links do not.. 
        """
        self.clerk.store(Record())
        actual =self.storage.match("Record")
        assert actual == [{"ID":1, "val":""}]

    def check_store_again(self):
        self.clerk.store(Record())
        r = self.clerk.fetch(Record, 1)
        r.val = "abc"
        self.clerk.store(r)

    def check_store_link(self):
        r = Record(val="a")
        r.next = Record(val="b")

        self.clerk.store(r)
        del r
        r = self.clerk.match(Record, val="a")[0]
        assert r.ID == 2, "didn't save links first!"
        assert r.next is not None, "didn't store the link"
        assert r.next.val=="b", "didn't store link correctly"

    def check_store_linksets(self):
        n = Node(data="a")
        n.kids << Node(data="aa")
        n.kids << Node(data="ab")
        n.kids[1].kids << Node(data="aba")

        self.clerk.store(n)
        del n
        n = self.clerk.match(Node, data="a")[0]
        assert n.ID == 1, "didn't save parent of linkset first!"
        assert len(n.kids)== 2, "didn't store the linkset"
        assert n.kids[0].data=="aa", "didn't store link correctly"
        assert n.kids[1].data=="ab", "didn't store link correctly"
        assert n.kids[1].kids[0].data=="aba", "didn't store link correctly"
        
        
    def check_fetch(self):
        self.clerk.store(Record(val="howdy"))
        obj = self.clerk.fetch(Record, 1)
        assert obj.val == "howdy"


    def check_delete(self):
        self.check_fetch()
        self.clerk.delete(Record, 1)
        assert self.storage.match("Record") == []


    def check_link_injection(self):
        self.storage.store("Record", val="a", nextID=2)
        self.storage.store("Record", val="b", nextID=3)
        self.storage.store("Record", val="c", nextID=None)

        a = self.clerk.fetch(Record, 1)
        
        assert a.val == "a"
        assert a.next.val == "b"
        assert a.next.next.val == "c"
        assert a.next.next.next is None


    def check_linkset_injection(self):
        self.storage.store("Node", data="top", parentID=None)
        self.storage.store("Node", data="a",   parentID=1)
        self.storage.store("Node", data="a.a", parentID=2)
        self.storage.store("Node", data="b",   parentID=1)
        
        top = self.clerk.fetch(Node, 1)
        assert top.kids[0].data == "a"
        assert top.kids[1].data == "b"
        assert top.kids[1].kids == []
        assert top.kids[0].kids[0].data == "a.a"

        

    def check_fetch_from_wide_table(self):
        """
        Supose a strongbox has 1 slot, but the table has 2+ columns.
        We can't just jam those columns into the strongbox,
        because strongbox is *designed* to blow up if you try
        to add new attributes.

        But on the other hand, a DBA should be able to add columns
        to the databaes without breaking the code and causing
        AttributeErrors all over the place.

        Instead, Clerk should only use the columns that have
        matching attributes, and simply ignore the others.

        This sorta violates the concept of OnceAndOnlyOnce,
        because now the tables can be out of sync with the
        data model, but I think it's better than the alternative,
        and this is the sort of thing one could check with
        an automated tool.

        #@TODO: write tool to compare DB and object models :)
        """
        try:
            self.storage.store("Record", val="a", extra_column="EEK!")
            a = self.clerk.fetch(Record, 1)
            a.val="aa"
            self.clerk.store(a)
        except AttributeError:
            self.fail("shouldn't die when columns outnumber attributes")





    def check_user(self):
        """
        @TODO: test case from cornerhost that exposed a bug
        also, the isInstance(LinkSetInjector) lines in Clerk.py
        don't seem to have test cases. And ought to do some kind
        of polymorphism magic anyway.
        """
        from cornerhost import *
        import cornerhost.config #@TODO: decouple from cornerhost
        clerk = Clerk(MockStorage(), cornerhost.config.dbMap)
        u = clerk.store(User(username="ftempy"))
        d = clerk.store(Domain(domain="ftempy.com", user=u))
        assert d.user, "didn't follow link before fetch"
        d = clerk.fetch(Domain, 1)
        assert d.user, "didn't follow link broke after fetch"
