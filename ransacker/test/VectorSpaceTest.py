"""
test cases for VectorSpace
"""

import unittest
from ransacker import VectorSpace
from ransacker.vectorspace.vecmath import normalize, magnitude, vcos, dcos
import math
from numpy import array


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
		

    def test_vectormath(self):

        '''
        For these tests, imagein that we have a 2-D graph of
        various "documents":

            x axis is the "dog" axis
            y axis is the "cat" axis

        We could then graph the following documents:

            b          a = 'cat'
            |          b = 'cat cat'
            a  c       c = 'dog cat'
            | /        d = 'dog'
            |/__d

        As you can see, the more similar two documents are,
        the smaller the angle between them. We can calculate
        this angle for any number of dimensions using the
        vcos() routine (thanks, linear algebra!)
        '''

        cat    = array([0,1])
        catcat = array([0,2])
        dogcat = array([1,1])
        dog    = array([1,0])

        assert magnitude(cat) == 1
        assert magnitude(catcat) == 2
        assert magnitude(dogcat) == math.sqrt(2) # a^2+b^2=c^2
        assert magnitude(dog) == 1

        def assertMatch(a,b):
            if not (a==b).all():
                raise AssertionError("%s != %s" % (a, b))

        assertMatch(normalize(cat), array([0,1]))
        assertMatch(normalize(catcat), array([0,1]))
        assertMatch(normalize(dogcat), array([1/math.sqrt(2), 1/math.sqrt(2)]))
        assertMatch(normalize(dog), array([1,0]))

        assert round(vcos(cat, cat), 3) == round(dcos(0),3)
        assert round(vcos(cat, catcat), 3) == round(dcos(0),3)
        assert round(vcos(cat, dogcat), 3) == round(dcos(45),3)
        assert round(vcos(cat, dog), 3) == round(dcos(90),3)


