"""
test cases for zikeshop.Style
"""
__ver__="$Id$"

import unittest
import zikeshop
import zdc
from zikeshop import Style
from arlo import MockClerk
clerk = MockClerk()

#@TODO: test picture attribute

class StyleTest(unittest.TestCase):

    def test_product(self):
        #@TODO: what's up with this test?
        # maybe it just tries not to get an error?
        style = clerk.fetch(Style, ID=2)
        prod = style.product
