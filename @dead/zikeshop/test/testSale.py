"""
test cases for zikeshop.Sale
"""
__ver__ = "$Id$"

import unittest
import zikeshop, zikebase

class SaleTestCase(unittest.TestCase):

    
    def check_links(self):
        sale = zikeshop.Sale()
        
        assert isinstance(sale.billAddress, zikebase.Contact),\
               "invalid billAddress"

        assert isinstance(sale.shipAddress, zikebase.Contact),\
               "invalid shipAddress"

        assert isinstance(sale.card, zikeshop.Card), \
               "invalid card"

        assert isinstance(sale.customer, zikeshop.Customer), \
               "invalid customer"
        
