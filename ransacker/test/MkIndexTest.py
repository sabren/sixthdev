"""
test cases for MkIndex
"""
__ver__="$Id$"

import os
from ransacker import MkIndex
from IndexTest import IndexTest

class MkIndexTest(IndexTest):

    def newIndex(self):
        return MkIndex()

    def check_file(self):
        name = "./spec/test"
        exts = [".rki", ".rkw", ".rkp"]
        for e in exts:
            if os.path.exists(name+e): os.unlink(name+e)
        idx = MkIndex(name)
        for e in exts:
            assert os.path.exists(name+e), "%s not found" % name+e
        
    def tearDown(self):
        pass
    
