"""
test cases for zikeshop.Style
"""
__ver__="$Id$"

import unittest
import zikeshop
import zdc
from zikeshop.test import clerk

#@TODO: test picture attribute

class StyleTestCase(unittest.TestCase):

    def check_product(self):
        #@TODO: what's up with this test?
        # maybe it just tries not to get an error?
        style = clerk.load(zikeshop.Style, ID=2)
        prod = style.product
