"""
test routines for the Parser class.

$Id$
"""
import unittest
import zebra

class ParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = zebra.Parser()
        
