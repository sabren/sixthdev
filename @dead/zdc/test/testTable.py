"""
testTable.py - test cases for zdc.Table

$Id$
"""

import unittest
import zdc.test
import zdc


class TableTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zdc.test.dbc.cursor()
        self.cur.execute("delete from test_fish")
        self.table = zdc.Table(zdc.test.dbc, "test_fish")

    def check_fields(self):
        assert (self.table.fields[0].name,
                self.table.fields[1].name) == ('ID', 'fish'), \
               "Table object doesn't get correct fields."


    def check_getRecord(self):
        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('squid')")
        rec = self.table.getRecord(ID=1)
        assert rec["fish"] == 'squid', \
               "table.getRecord doesn't return the correct record."
       

    def tearDown(self):
        del self.cur
        


