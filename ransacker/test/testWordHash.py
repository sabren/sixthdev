"""
testWordHash.py - tests for ransacker's WordHash class

$Id$
"""

import ransacker
import unittest
import os

class WordHashTestCase(unittest.TestCase):

    def setUp(self):
        self.hash = ransacker.WordHash("test/test.rkw")
        self.hash.add("ant")
        self.hash.add("box")
        self.hash.add("car")
        self.hash.add("dog")


    def check_keys(self):
        keys = self.hash.keys()
        keys.sort()
        assert keys == ['ant', 'box', 'car', 'dog'], \
               "Doesn't return the correct keys!"


    def check_add(self):
        try:
            gotError = 0
            self.hash.add("ant")
        except KeyError:
            gotError = 1

        assert gotError, ".add(word) doesn't complain when word already exists."


    def check_values(self):
        assert (self.hash["ant"] == 1) and (self.hash["dog"] == 4), \
               "WordHash doesn't autonumber correctly"
    

    def check_setitem(self):
        try:
            gotError = 0
            self.hash["egg"] = 5
        except KeyError:
            gotError = 1

        assert gotError, "wordHash[xxx] = yy works, but it should raise an error"
        

    def tearDown(self):
        del self.hash
        os.remove("test/test.rkw")
