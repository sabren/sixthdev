
from storage import Storage
import unittest


class OldMatcher(Storage):
    def _match(self, table, whereClause, orderBy):
        self.clause = whereClause


class StorageTest(unittest.TestCase):

    def test_oldmatch(self):
        o = OldMatcher()
        o.match("blah", ID=5)
        self.assertEquals( str(o.clause), "(ID = '5')")
        


if __name__=="__main__":
    unittest.main()
