"""
test cases for MkIndex
"""
__ver__="$Id$"

import os
from ransacker import SQLiteIndex
from IndexTest import IndexTest

class SQLiteIndexTest(IndexTest):

    def newIndex(self):
        path = "spec/sqlite.rk"
        if os.path.exists(path):
            os.unlink(path)
        return SQLiteIndex(path)


    def tearDown(self):
        self.idx.close()
        os.unlink("spec/sqlite.rk")
