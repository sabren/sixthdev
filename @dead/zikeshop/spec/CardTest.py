"""
test cases for zikeshop.Card
"""
__ver__ = "$Id$"

import unittest
import zikeshop
from zikeshop.test import clerk
from zikeshop import Card

class CardTestCase(unittest.TestCase):

    #@TODO: really test the validation stuff!

    def setUp(self):
        
        # a little game of good card, bad card...
        # this card is unlikely, but passes the mod10 check:
        self.GOODCARD = '4111111111111111'
        self.BADCARD  = '4111111111111119' 
    
    def check_masked(self):
        card = Card()
        card.number = self.GOODCARD
        assert card.masked == 'xxxxxxxxxxxx1111', \
               "masking doesn't work: %s" % card.masked

    def check_checkdigits(self):
        """
        check the checker..
        """
        card = Card()
        assert card.checkdigits(self.GOODCARD) == 1, \
               "check of good card failed..."

        assert card.checkdigits(self.BADCARD) == 0, \
               "check of bad card failed to fail... :)"
        
        
