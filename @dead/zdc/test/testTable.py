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

    def check_quotes(self):
        table = zdc.Table(zdc.test.dbc, "test_fish")
        assert table._sqlQuote(table.fields["fish"], "foo'fish") \
               == "'foo\\'fish'", \
               "quoting failed for STRING"
        assert table._sqlQuote(table.fields["ID"], 0) == "0",\
               "quotes failed for NUMBER"
        # @TODO: test BINARY .. but what should it do?



    def check_fetch(self):
        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('squid')")
        rec = self.table.fetch(1)
        assert rec["fish"] == 'squid', \
               "table.getRecord doesn't return the correct record."
       
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


    def tearDown(self):
        del self.cur
        


