"""
test cases for MkIndex
"""
__ver__="$Id$"

import os
from ransacker import SQLiteIndex
from IndexTest import IndexTest

class SQLiteIndexTest(IndexTest):

    def newIndex(self):
        return SQLiteIndex("spec/sqlite.rk")


    def tearDown(self):
        self.idx.close()
        os.unlink("spec/sqlite.rk")
