
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

