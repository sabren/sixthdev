#
# testRecord.py - test cases for zdc.Record

import unittest
import test
import zdc


class RecordTestCase(unittest.TestCase):

    ## module: zdc.Record

    def win32check_ModuleGuess(self):
        import winODBCdb
        conn = winODBCdb.connect("testzdc")
        rec = zdc.Record(conn, "testzdc_fish")
        assert rec.dbcModule == winODBCdb, "dbcModule failed for winODBCdb"


    def win32check_ModuleTell(self):
        # check that TELLING it which module to use works..
        import ODBC.Windows
        conn = ODBC.Windows.connect("testzdc")
        raisedAnError = 0
        try:
            rec = zdc.Record(conn, "testzdc_fish")
        except:
            raisedAnError = 1
        # note: this test would fail if ODBC.Windows ever got a .__class__
        assert raisedAnError, "dbcModule shoulda given an error for ODBC.Windows"

        # now test the proper use:
        rec = zdc.Record(conn, "fish", module=ODBC.Windows)


    def setUp(self):
        cur = test.dbc.cursor()
        try:
            cur.execute("DROP TABLE fish")
        except:
            pass
        cur.execute("""
           CREATE TABLE fish (
              ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
              fish VARCHAR(32)
           )
           """)

    def check_fields(self):
        rec = zdc.Record(test.dbc, "fish")
        assert rec.fields[0].name == "ID", "ID not first field"
        assert rec.fields[1].name == "fish", "fish not second field"


    def check_quotes(self):
        rec = zdc.Record(test.dbc, "fish")
        assert rec._sqlQuote(rec.fields["fish"], "foo'fish") == "'foo''fish'", \
               "quoting failed for STRING"
        rec.quoteEscape = '\\'
        assert rec._sqlQuote(rec.fields["fish"], "foo'fish") == "'foo\\'fish'", \
               "quoteEscape failed"
        assert rec._sqlQuote(rec.fields["ID"], 0) == "0",\
               "quotes failed for NUMBER"
        # @TODO: test BINARY .. but what should it do?


    def check_insert(self):
        rec = zdc.Record(test.dbc, "fish")
        rec.new()
        rec['fish'] = 'salmon'
        rec.save()
        assert rec['ID'] is not None, "didn't get an ID"


    def tearDown(self):
        pass
