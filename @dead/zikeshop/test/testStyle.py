"""
test cases for zikeshop.Style
"""
__ver__="$Id$"

import unittest
import zikeshop
import zikeshop.test
import zdc

#@TODO: test picture attribute

class StyleTestCase(unittest.TestCase):

    def setUp(self):
        self.ds = zikeshop.test.dbc
        self.cur = zikeshop.test.dbc.cursor()

    def check_product(self):
        #@TODO: what's up with this test?
        # maybe it just tries not to get an error?
        style = zikeshop.Style(self.ds, ID=2)
        prod = style.product
