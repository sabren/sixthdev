"""
test cases for zikeshop.Card
"""
__ver__ = "$Id$"

import unittest
import zikeshop

class CardTestCase(unittest.TestCase):

    def check_masked(self):
        card = zikeshop.Card()
        card.number =         '0123456789ABCDEF'
        assert card.masked == 'xxxxxxxxxxxxCDEF', \
               "masking doesn't work: %s" % card.masked
