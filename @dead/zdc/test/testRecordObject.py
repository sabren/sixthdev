#
# testRecordObject.py - test cases for zdc.RecordObject

import unittest
import zdc.RecordObject
import test

class RecordObjectTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = test.dbc.cursor()
        try:
            self.cur.execute("DROP TABLE fish")
        except:
            pass
        self.cur.execute("""
           CREATE TABLE fish (
              ID int not null auto_increment primary key,
              fish varchar(32)
           )
        """)
        

    def check_table(self):
        
        ## part1: table from the constructor
        robj = zdc.RecordObject(test.dbc, table="fish")
        assert robj.table == "fish", "table passed to constructor didn't work."
        del robj

        ## part2: table from __class__.table
        class Fish(zdc.RecordObject):
            table="fish"

        robj = Fish(test.dbc)
        assert robj.table == "fish", "__class__.table didn't work."



    def check_save(self):
        robj = zdc.RecordObject(test.dbc, table="fish")
        robj.fish = 'trout'
        robj.save()

        assert robj.ID == 1, "ID not updated after save()"

        self.cur.execute("SELECT ID, fish FROM fish WHERE fish='trout'")
        assert self.cur.fetchone() == (1, 'trout'), "save() didn't add record correctly."


    def tearDown(self):
        del self.cur
        


