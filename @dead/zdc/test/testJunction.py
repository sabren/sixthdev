"""
unit tests for zdc.Junction
"""
__ver__="$Id$"
import unittest
import zdc
from strongbox import attr

class Left(zdc.RecordObject):
    """
    A test class for a Junction.
    """
    __super = zdc.RecordObject
    _tablename = "test_left"
    ID = attr(long)

    def _new(self):
        self._super._new(self)
        self.name=""

    #@TODO: is this really the best way to do this?
    def get_rights(self):
        if not self._data.has_key("rights"):
            self._data["rights"] = zdc.Junction(self, Left,
                                                "test_left_right",
                                                "leftID", "rightID")
            self._data["rights"].fetch()
        return self._data["rights"]


class Right(zdc.RecordObject):
    """
    Another test class for use with Junction.
    """
    __super = zdc.RecordObject
    _tablename = "test_right"
    ID = attr(long)

    def _new(self):
        self._super._new(self)
        self.name=""
    

class JunctionTestCase(unittest.TestCase):

    #@TODO: put test cases here!
    # (they're not here because I factored junction out of
    # zikeshop.Product and zikeshop.Category, and relied on
    # the unit tests for those objects to do so.)

    def setUp(self):
        self.ds = zdc.test.dbc
        self.cur = self.ds.cursor()
        self.cur.execute("DELETE FROM test_left")
        self.cur.execute("DELETE FROM test_right")
        self.cur.execute("DELETE FROM test_left_right")
        self.cur.execute("INSERT INTO test_left  VALUES (1, 'uno')")
        self.cur.execute("INSERT INTO test_left  VALUES (2, 'dos')")
        self.cur.execute("INSERT INTO test_right VALUES (1, 'one')")
        self.cur.execute("INSERT INTO test_right VALUES (2, 'two')")
        self.cur.execute("INSERT INTO test_left_right VALUES (1,2,1)")
        self.cur.execute("INSERT INTO test_left_right VALUES (2,2,2)")

    def check_fetch(self):

        # case a: nothing in the join
        assert len(Left(self.ds, ID=1).rights) == 0, \
               "got Rights in empty junction.."

        actual = len(Left(self.ds, ID=2).rights)
        assert actual==2, \
               "expected 2 Rights in junction, got %s" % actual

