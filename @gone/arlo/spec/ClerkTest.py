
from arlo import Clerk
from storage import MockStorage
from strongbox import Strongbox, attr, link
import unittest


class Record(Strongbox):
    ID = attr(long)
    val = attr(str)
    next = link("Record")
    

class ClerkTest(unittest.TestCase):

    def setUp(self):
        self.storage = MockStorage()
        self.clerk = Clerk(self.storage)
        # @TODO: figure out how to let me use Record.next here..
        self.clerk.dbmap[Record.__attrs__['next']] = (Record, 'nextID')

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
        
    def check_fetch(self):
        self.clerk.store(Record(val="howdy"))
        obj = self.clerk.fetch(Record, 1)
        assert obj.val == "howdy"


    def check_delete(self):
        self.check_fetch()
        self.clerk.delete(Record, 1)
        assert self.storage.match("Record") == []


    def check_links(self):
        self.storage.store("Record", val="a", nextID=2)
        self.storage.store("Record", val="b", nextID=3)
        self.storage.store("Record", val="c", nextID=None)

        a = self.clerk.fetch(Record, 1)
        
        assert a.val == "a"
        assert a.next.val == "b"
        assert a.next.next.val == "c"
        assert a.next.next.next is None


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
