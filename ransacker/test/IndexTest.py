"""
test cases for Index
"""

import unittest
from ransacker import Index

class IndexTest(unittest.TestCase):

    def newIndex(self):
        return Index()

    def setUp(self):
        self.idx = self.newIndex()
        self.idx.addDocument("onedog", "my dog has fleas")
        self.idx.addDocument("cathat", "the cat in the hat")
        self.idx.addDocument("twodog", "it's a dog eat dog world")

    def check_contains(self):
        assert self.idx.contains("cathat")
        assert self.idx.contains("onedog")
        assert not self.idx.contains("bigdog")
        assert not self.idx.contains("oaktree")


    def check_match(self):
        actual = self.idx.match('dog')
        assert ('onedog' in actual) and ('twodog' in actual), \
               "match() doesn't find things: %s" % str(actual)
        assert actual == ('twodog', 'onedog'), \
               "match() doesn't use relevance: %s" % str(actual)
