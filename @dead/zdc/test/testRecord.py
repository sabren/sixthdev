"""
test cases for zdc.Record
"""
__ver__="$Id$"

import unittest
import zdc.test
import zdc


class RecordTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zdc.test.dbc.cursor()
        self.cur.execute("delete from test_fish")
        self.cur.execute("delete from test_types")
        self.table = zdc.Table(zdc.test.dbc, "test_fish")

    def check_fetch(self):
        self.cur.execute("INSERT INTO test_fish (fish) VALUES ('pufferfish')")
        rec = self.table.fetch(1)

        assert rec["fish"] == 'pufferfish', \
               "didn't fetch correct record!"
        
    def check_insert(self):
        #@TODO: make this read self.table.new()
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
        rec = self.table.fetch(1)
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
        rec = self.table.fetch(1)
        assert (not rec.isNew), "existing record is considered new!"
        

    def check_types(self):
        fInt = 5982374
        fString = "this\\'is'\na string"

        # text and blob are really the same, at least on MySQL,
        # but we'll test them both anyway..
        import string
        fText = string.join(map(chr, range(256)),'') # test all ASCII characters
        fBlob = fText + open('test/testRecord.pyc',"r").read() # our own bytecodes :)

        rec = zdc.Record(zdc.Table(zdc.test.dbc, "test_types"))
        rec["f_int"] = fInt
        rec["f_string"] = fString
        rec["f_text"] = fText
        rec["f_blob"] = fBlob
        rec.save()

        # test that it WRITES them correctly:
        self.cur.execute(
            "SELECT f_int, f_string, f_text, f_blob from test_types where ID=1")

        row = self.cur.fetchone()
        assert row is not None, \
               "Record didn't write data at all!"
        assert row[0] == fInt, \
               "Record doesn't save ints correctly"
        assert row[1] == fString, \
               "Record doesn't save strings correctly"

        for i in range(len(fText)):
            assert row[2][i] == fText[i], \
                   "Record: saves chr(%s) wrong in text fields. (got: %s wanted: %s)" \
                   % (i, repr(row[2][i]), repr(fText[i]))

        assert row[2] == fText, \
               "Record doesn't save texts correctly"


        assert row[3] == fBlob, \
               "Record doesn't save blobs correctly"
        
        
        # also test that it READS them correctly:
        rec = zdc.Table(zdc.test.dbc, "test_types").fetch(1)
        assert rec["f_int"] == fInt, \
               "Record doesn't retrieve ints correctly."
        assert rec["f_string"] == fString, \
               "Record doesn't retrieve strings correctly."
        assert rec["f_text"] == fText, \
               "Record doesn't retrieve texts correctly."
        assert rec["f_blob"] == fBlob, \
               "Record doesn't retrieve blobs correctly."
        


    def check_manyRecs(self):
        """Do multiple records accidentally conflict with each other?"""
        import copy
        
        rec = zdc.Record(self.table)
        rec['fish'] = 'snagglefish' # whassat?
        rec.save()
        firstID = copy.copy(rec['ID'])

        rec2 = zdc.Record(self.table)
        rec2['fish'] = 'babelfish'
        rec2.save()

        assert rec['ID'] == firstID, \
               "uh-oh! rec's ID changed!: %s, %s" % (rec['ID'], firstID)


##     def check_dates(self):
##         self.cur.execute("insert into test_types (sometime) values (now())")
##         rec = zdc.Record(zdc.Table(zdc.test.dbc, "test_types"), ID=1)
##         # nothing to assert, but this was/is causing an error:
##         rec.save()
##
##         # actually, I turned off all date handling stuff altogether for
##         # the time being, because it was disabling zikeshop... :/
##         raise "@TODO: figure out how to support dates!"

        
    def tearDown(self):
        pass

