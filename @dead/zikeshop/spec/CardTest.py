"""
test cases for zikeshop.Card
"""
__ver__ = "$Id$"

import unittest
import zikeshop

class CardTestCase(unittest.TestCase):

    def setUp(self):
        # a little game of good card, bad card...
        # this card is unlikely, but passes the mod10 check:
        self.GOODCARD = '41111111111111113'
        self.BADCARD  = '41111111111111111' 
    
    def check_masked(self):
        card = zikeshop.Card() 
        card.number = self.GOODCARD
        assert card.masked == 'xxxxxxxxxxxxx1113', \
               "masking doesn't work: %s" % card.masked

    def check_checkdigits(self):
        """
        check the checker..
        """
        card = zikeshop.Card()
        assert card.checkdigits(self.GOODCARD) == 1, \
               "check of good card failed..."

        assert card.checkdigits(self.BADCARD) == 0, \
               "check of bad card failed to fail... :)"
        
        
