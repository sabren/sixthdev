"""
test cases for zikeshop.Sale
"""
__ver__ = "$Id$"

import unittest
import zikeshop
from zikeshop import Contact
from zikeshop import Sale
from zikeshop.test import clerk

class SaleTestCase(unittest.TestCase):

    
    def check_links(self):
        sale = clerk.new(Sale)
        
        assert isinstance(sale.billAddress, Contact),\
               "invalid billAddress"

        assert isinstance(sale.shipAddress, Contact),\
               "invalid shipAddress"

        assert isinstance(sale.card, zikeshop.Card), \
               "invalid card"

        assert isinstance(sale.customer, Contact), \
               "invalid customer"
        
