"""
test cases for VectorSpace
"""

import unittest
from ransacker import VectorSpace

class VectorSpaceTest(unittest.TestCase):

    def setUp(self):
	pass


    def test_everything(self):

        docs = ["dog", "cat", "dog? cat", "cat cat"]
        idx = VectorSpace(docs)
        idx.build_index()
        assert idx.getWordList() == ["cat", "dog"]

        engine = idx.getEngine()
        results = engine.search("dog")
        assert results.has_key("dog")
        assert results.has_key("dog? cat")
        assert len(results.keys()) == 2
        assert results["dog"] > results["dog? cat"]
		
