"""
testTable.py - test cases for zdc.Table
"""
__ver__="$Id$"

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

    def check_fetch(self):
        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('squid')")
        rec = self.table.fetch(1)
        assert rec["fish"] == 'squid', \
               "table.getRecord doesn't return the correct record."

        del rec
        rec = self.table.fetch(ID=1)
        assert rec["fish"] == 'squid', \
               "didn't return correct record when using a string key.."

        # don't do this for real, kids.. :)
        self.table.rowid='fish'
        del rec
        rec = self.table.fetch('squid')
        assert rec["fish"] == 'squid', \
               "didn't return correct record when using a string key.."
       
    def check_select(self):       
        for item in ["haddock", "lamprey", "stingray", "trout"]:
            self.cur.execute("INSERT INTO test_fish (fish) VALUES ('%s')"
                             % item)

        recs = self.table.select()
        assert len(recs) == 4, \
               "wrong records returned on select all: %s" % len(recs)

        recs = self.table.select("fish <> 'trout'")
        assert len(recs) == 3, \
               "wrong records returned after SQL: %s" % len(recs)

        recs = self.table.select(fish="haddock")
        assert len(recs) == 1, \
               "wrong records returned after keywords: %s" % len(recs)


    def check_delete(self):
        self.cur.execute("insert into test_fish (fish) values ('piranha')")
        self.table.delete(1)
        recs = self.table.select()
        assert len(recs) == 0, \
               "didn't delete record..."

    def tearDown(self):
        del self.cur
        


