"""
test cases for MkIndex
"""
__ver__="$Id$"

import os
import unittest
from ransacker import MkIndex

class MkIndexTest(unittest.TestCase):

    def setUp(self):
        self.idx = MkIndex()
        self.idx.add("onedog", "my dog has fleas")
        self.idx.add("cathat", "the cat in the hat")
        self.idx.add("twodog", "it's a dog eat dog world")

    def check_match(self):
        actual = self.idx.match('dog')
        assert ('onedog' in actual) and ('twodog' in actual), \
               "match() doesn't find things: %s" % str(actual)
        assert actual == ('twodog', 'onedog'), \
               "match() doesn't use relevance: %s" % str(actual)

    def check_score(self):
        actual = self.idx.score("dog")
        self.assertEquals(actual, (('twodog', 2), ('onedog',1)))


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
    
