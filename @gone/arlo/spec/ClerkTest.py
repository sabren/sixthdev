
from arlo import Clerk, Schema
from storage import MockStorage
from strongbox import Strongbox, attr, link, linkset, forward
import unittest

class Record(Strongbox):
    ID = attr(long)
    val = attr(str)
    next = link(forward)
Record.next.type=Record

class Node(Strongbox):
    ID = attr(long)
    data = attr(str)
    parent = link(forward)
    kids = linkset(forward, "parent")
Node.kids.type=Node
Node.parent.type=Node   


class ClerkTest(unittest.TestCase):

    def setUp(self):
        self.storage = MockStorage()
        schema = Schema({
            Node: "Node",
            Node.parent: "parentID",
            Record: "Record",
            Record.next: "nextID",
        })
        self.clerk = Clerk(self.storage, schema)


    def test_store(self):
        self.clerk.store(Record())
        actual = self.storage.match("Record")
        assert actual == [{"ID":1, "val":"", "nextID":0}], actual
        r = self.clerk.fetch(Record, 1)
        assert r.next is None
        

    def test_store_again(self):
        self.clerk.store(Record())
        r = self.clerk.fetch(Record, 1)
        r.val = "abc"
        self.clerk.store(r)

    def test_store_link(self):
        r = Record(val="a")
        r.next = Record(val="b")

        self.clerk.store(r)
        del r
        r = self.clerk.match(Record, val="a")[0]
        assert r.ID == 2, "didn't save links first!"
        assert r.next is not None, "didn't store the link"
        assert r.next.val=="b", "didn't store link correctly"

        r.next = None
        self.clerk.store(r)
        r = self.clerk.match(Record, val="a")[0]
        assert r.next is None, "didn't delete link!"

        r = Record(val="noNext")
        self.clerk.store(r)
        r = self.clerk.fetch(Record, val="noNext")
        assert r.next is None


    def test_store_memo(self):
        rb = self.clerk.store(Record(val="b"))
        ra = self.clerk.store(Record(val="a", next=rb))

        a,b = self.clerk.match(Record, orderBy="val")
        assert a is ra
        assert b is rb


    def test_store_linksets(self):
        n1 = Node(data="a")
        n1.kids << Node(data="aa")
        n1.kids << Node(data="ab")
        n1.kids[1].kids << Node(data="aba")
        self.clerk.store(n1)
        assert len(n1.kids)== 2, [(k.ID, k.data) for k in n1.kids]        
        
        n = self.clerk.fetch(Node, data="a")
        assert len(n1.kids)== 2, "fetch corrupted kids: %s" % [(k.ID, k.data) for k in n1.kids]
        
        assert n.ID == 1, "didn't save parent of linkset first!"
        assert len(n.kids)== 2, "didn't store the linkset: %s" % [(k.ID, k.data) for k in n.kids]
        assert n.kids[0].data=="aa", "didn't store link correctly"
        assert n.kids[1].data=="ab", "didn't store link correctly"
        assert n.kids[1].kids[0].data=="aba", "didn't store link correctly"
        assert n.kids[0].parent is n
        assert n.kids[1].parent is n

        n.kids[1].parent=None
        n.kids.remove(n.kids[1])
        self.clerk.store(n)
        n = self.clerk.match(Node, data="a")[0]
        assert len(n.kids) == 1

        
        
    def test_fetch(self):
        self.clerk.store(Record(val="howdy"))

        # we can pass in an ID:
        obj = self.clerk.fetch(Record, 1)
        assert obj.val == "howdy"

        # or we can use keywords:
        obj = self.clerk.fetch(Record, val="howdy")
        assert obj.val == "howdy"


    def test_delete(self):
        self.test_fetch()
        self.clerk.delete(Record, 1)
        assert self.storage.match("Record") == []


    def test_link_injection(self):
        self.storage.store("Record", val="a", nextID=2)
        self.storage.store("Record", val="b", nextID=3)
        self.storage.store("Record", val="c", nextID=None)

        a = self.clerk.fetch(Record, 1)
        
        assert a.val == "a"
        assert a.next.val == "b"
        assert a.next.next.val == "c"
        assert a.next.next.next is None


    def test_linkset_injection(self):
        self.storage.store("Node", data="top", parentID=None)
        self.storage.store("Node", data="a",   parentID=1)
        self.storage.store("Node", data="a.a", parentID=2)
        self.storage.store("Node", data="b",   parentID=1)
        
        top = self.clerk.fetch(Node, 1)
        assert top.kids[0].data == "a"
        assert top.kids[1].data == "b"
        assert top.kids[1].kids == []
        assert top.kids[0].kids[0].data == "a.a"

        

    def test_fetch_from_wide_table(self):
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

    def test_dirt(self):
        # dirty by default (already tested in strongbox)
        r = Record()
        assert r.private.isDirty

        # but not after a store:
        r = self.clerk.store(r)
        assert not r.private.isDirty

        # and not after a fetch:
        r = self.clerk.fetch(Record, ID=1)
        assert not r.private.isDirty

        # or a match:
        r = self.clerk.match(Record)[0]
        assert not r.private.isDirty


    def test_recursion(self):
        r = Record()
        r.next = Record()
        r.next.next = r
        assert r.private.isDirty
        assert r.next.private.isDirty
        r = self.clerk.store(r)
        assert r.ID == 2
        assert r.next.ID == 1

        r = self.clerk.fetch(Record, 2)
        assert not r.private.isDirty
        assert not r.next.private.isDirty


        ## and the same thing for linksets:
        n = Node()
        n.kids << Node()
        n.kids[0].kids << n
        assert n.private.isDirty
        assert n.kids[0].private.isDirty
        n = self.clerk.store(n)
        
        
    def test_identity(self):
        self.clerk.store(Record(val="one"))
        rec1a = self.clerk.fetch(Record, 1)
        rec1b = self.clerk.fetch(Record, 1)
        assert rec1a is rec1b

        n = Record()
        r = Record(next=n)        
        assert self.clerk.store(r) is r
        assert self.clerk.cache[(Record, r.ID)] is r
        assert self.clerk.cache[(Record, n.ID)] is n
        assert self.clerk.cache[(Record, n.ID)] is r.next

    def test_stub(self):
        self.clerk.store(Record(val="a", next=Record(val="b")))
        self.clerk.cache.clear()
        recA = self.clerk.fetch(Record, val="a")
        recB = self.clerk.fetch(Record, val="b")
        assert recA.next.ID == recB.ID
        assert recA.next is recB

    def test_match(self):
        self.clerk.store(Record(val="one"))
        self.clerk.store(Record(val="two"))
        self.clerk.store(Record(val="two"))
        assert len(self.clerk.match(Record, val="zero")) == 0
        assert len(self.clerk.match(Record, val="one")) == 1
        assert len(self.clerk.match(Record, val="two")) == 2
        
    def test_matchOne(self):
        self.clerk.store(Record(val="one"))
        self.clerk.store(Record(val="two"))
        self.clerk.store(Record(val="two"))
        
        try:
            self.clerk.matchOne(Record, val="zero")
            self.fail("should have failed for not matching")
        except LookupError: pass

        assert isinstance(self.clerk.matchOne(Record, val="one"),
                          Record)

        try:
            self.clerk.matchOne(Record, val="two")
            self.fail("should have failed for matching two")
        except LookupError: pass
        
