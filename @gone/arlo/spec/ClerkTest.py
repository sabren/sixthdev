
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

    def check_dirt(self):
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


    def check_recursion(self):
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
        
        

    def check_complex_recursion(self):
        """
        test case from cornerhost that exposed a bug.
        this is probably redundant given check_recursion
        but it doesn't hurt to keep it around. :)

        This test is complicated. Basically it sets up
        several classes that refer to each other in a loop
        and makes sure it's possible to save them without
        infinite recursion.
        
        @TODO: isInstance(LinkSetInjector) in Clerk.py need tests
        It ought to do some kind of polymorphism magic anyway.
        (huh??)
        """

        class User(Strongbox):
            ID = attr(long)
            username = attr(str)
            domains = linkset(forward)
            sites = linkset(forward)
        class Domain(Strongbox):
            ID = attr(long)
            user = link(User)
            name = attr(str)
            site = link(forward)            
        class Site(Strongbox):
            ID = attr(long)
            user = link(User)
            domain = link(Domain)
        User.__attrs__["domains"].type = Domain
        User.__attrs__["sites"].type = Site
        Domain.__attrs__["site"].type = Site
        dbMap = {
            User:"user",
            User.__attrs__["domains"]: (Domain, "userID"),
            User.__attrs__["sites"]: (Site, "userID"),
            Domain:"domain",
            Domain.__attrs__["user"]: (User, "userID"),
            Domain.__attrs__["site"]: (Site, "siteID"),
            Site:"site",
            Site.__attrs__["user"]: (User, "userID"),
            Site.__attrs__["domain"]: (Domain, "domainID"),
            }
       
        clerk = Clerk(MockStorage(), dbMap)
        u = clerk.store(User(username="ftempy"))
        u = clerk.match(User,username="ftempy")[0]
        d = clerk.store(Domain(name="ftempy.com", user=u))
        assert d.user, "didn't follow link before fetch"
        d = clerk.match(Domain, name="ftempy.com")[0]

        # the bug was here: it only happened if User had .domains
        # I think because it was a linkset, and the linkset had
        # an injector. Fixed by breaking the test for
        # hasInjectors out of an "and" and into the body of the
        # if block, in Clerk.store()
        assert d.user, "didn't follow link after fetch"
        assert d.user.ID == u.ID

        # ah, but then we had an infinite recursion problem
        # with site, but I fixed that with private.isDirty:
        d.site = clerk.store(Site(domain=d))
        d = clerk.store(d)
        assert d.site.domain.name == "ftempy.com"

        # and again here:
        d = clerk.fetch(Domain, 1)
        assert not d.private.isDirty
        assert not d.site.private.isDirty # this failed.
        clerk.store(d)                    # so this would recurse forever
