"""
test cases for Index
"""

import unittest
from ransacker import Index

class IndexTest(unittest.TestCase):

    def setUp(self):
	pass

    def check_addDocument(self):
	idx = Index()
        idx.addDocument("cat", "cat")
        idx.addDocument("catdog", "cat dog")
        assert idx.contains("cat")
        assert idx.contains("catdog")
        assert not idx.contains("dog")
        #assert not idx.contains("platypus")



