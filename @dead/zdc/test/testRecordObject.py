"""
testRecordObject.py - test cases for zdc.RecordObject
"""
__ver__="$Id$"

import unittest
import zdc.test
import zdc

class Fish(zdc.RecordObject):
    _tablename="test_fish"

class RecordObjectTestCase(unittest.TestCase):

    def setUp(self):
        self.ds = zdc.test.dbc
        self.cur = zdc.test.dbc.cursor()
        self.cur.execute("delete from test_fish")
        

    def check_table(self):
        ## table from __class__._tablename

        robj = Fish(self.ds)
        assert robj._table.name == "test_fish", \
               "__class__._tablename didn't work."


    def check_insert(self):
        robj = Fish(self.ds)
        robj.fish = 'trout'
        robj.save()

        assert robj.ID == 1, "ID not updated after save()"

        self.cur.execute("SELECT ID, fish FROM test_fish WHERE fish='trout'")
        assert self.cur.fetchone() == (1, 'trout'), \
               "save() didn't add record correctly."


    def check_update(self):
        self.cur.execute(
            "INSERT INTO test_fish (ID, fish) VALUES (5, 'fluunder (sic)')")

        robj = Fish(self.ds, ID=5)
        robj.fish = 'flounder'
        robj.save()

        self.cur.execute("SELECT fish from test_fish WHERE ID=5")
        assert self.cur.fetchone() == ('flounder',), \
               "save() didn't update record correctly!"
        


    def check_fetch(self):
        self.cur.execute("insert into test_fish (fish) values ('guppy')")
        robj = Fish(self.ds, ID=1)

        assert robj.ID == 1, "didn't fetch correct ID"
        assert robj.fish == 'guppy', "didn't fetch correct 'fish' field."

        del robj
        ## test search by non-key field..
        ## (essential for, say, the zikeshop product/category pages)
        robj = Fish(self.ds, fish='guppy')       
        assert robj.ID == 1, "didn't fetch correct ID after select by name"
        assert robj.fish == 'guppy', "didn't fetch correct 'fish' field."

    def check_saveTwice(self):

        # created this test because it used to give DuplicateError
        
        robj = Fish(self.ds)

        robj.fish = 'eel'
        robj.save()

        try:
            gotError = 0
            robj.fish = 'electric eel'
            robj.save()
        except:
            gotError = 1

        assert not gotError, \
               "problem saving RecordObject twice!"

## ## I removed this test because I don't think it applies
## ## anymore.. does it?  actually, there should be SOME kind of error
## ## if you try to select a record that isn't there, but probably not
## ## a KeyError.. maybe NotFoundError?
## ##
## ## .. you'd also never pass in a numeric key anymore..
## ## it would be RecordObject(self.table, ID=55)
##        
##     def check_invalidKey(self):
##         try:
##             gotError = 0
##             robj = zdc.RecordObject(self.table, 55)
##         except KeyError:
##             gotError = 1
##
##         assert gotError, "invalid key doesn't throw KeyError :/"



    def tearDown(self):
        del self.cur
