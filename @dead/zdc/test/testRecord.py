#
# testRecord.py - test cases for zdc.Record

import unittest
import zdc.test
import zdc


class RecordTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zdc.test.dbc.cursor()
        self.cur.execute("delete from test_fish")
        self.table = zdc.Table(zdc.test.dbc, "test_fish")


    def check_quotes(self):
        rec = zdc.Record(self.table)
        assert rec._sqlQuote(rec.table.fields["fish"], "foo'fish") == "'foo''fish'", \
               "quoting failed for STRING"
        rec.quoteEscape = '\\'
        assert rec._sqlQuote(rec.table.fields["fish"], "foo'fish") == "'foo\\'fish'", \
               "quoteEscape failed"
        assert rec._sqlQuote(rec.table.fields["ID"], 0) == "0",\
               "quotes failed for NUMBER"
        # @TODO: test BINARY .. but what should it do?


    def check_fetch(self):
        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('pufferfish')")
        rec = zdc.Record(self.table, ID=1)

        assert rec["fish"] == 'pufferfish', \
               "didn't fetch correct record!"
        
    def check_insert(self):
        rec = zdc.Record(self.table)
        rec['fish'] = 'salmon'
        rec.save()

        self.cur.execute('select count(*) from test_fish')
        assert self.cur.fetchone() == (1,), "didn't insert record!"

    def check_autonum(self):
        rec = zdc.Record(self.table)
        rec['fish'] = 'seahorse'
        rec.save()

        assert rec['ID'] == 1, "didn't get an ID"


    def check_update(self):
        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('glo_fish')")
        rec = zdc.Record(self.table, ID=1)
        rec["fish"] = "glowfish"
        rec.save()
        
        self.cur.execute("SELECT fish FROM test_fish WHERE ID=1")
        assert self.cur.fetchone() == ('glowfish',), \
               "didn't update correctly!"


    def check_savetwice(self):
        # this used to give a DuplicateError

        rec = zdc.Record(self.table)
        rec["fish"] = "onefish"
        rec.save()

        rec["fish"] = "twofish"
        rec.save()


    def check_isNew(self):
        rec = zdc.Record(self.table)
        assert rec.isNew, "New record doesn't have true .isNew"

        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('silverfish [ugh!]')")
        rec = zdc.Record(self.table, ID=1)
        assert (not rec.isNew), "existing record is considered new!"
        

    def tearDown(self):
        pass



