
from arlo import Clerk
from storage import MockStorage
from strongbox import Strongbox, attr
import unittest

class Record(Strongbox):
    ID = attr(long)
    val = attr(str)
    

class ClerkTest(unittest.TestCase):

    def setUp(self):
        self.storage = MockStorage()
        self.clerk = Clerk(self.storage)

    def check_store(self):
        self.clerk.store(Record())
        assert self.storage.match("Record") == [{"ID":1, "val":""}]
        
    def check_fetch(self):
        self.clerk.store(Record(val="howdy"))
        obj = self.clerk.fetch(Record, 1)
        assert obj.val == "howdy"
        
    def check_delete(self):
        self.check_fetch()
        self.clerk.delete(Record, 1)
        assert self.storage.match("Record") == []
