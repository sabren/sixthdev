"""
test cases for zikeshop.Sale
"""
__ver__ = "$Id$"

import unittest
import zikeshop
from zikeshop import Contact
from zikeshop import Sale

class SaleTest(unittest.TestCase):

    def check_links(self):
        raise "skip"  # by default, these are now null.
        #@TODO: should I create blank objects in __init__ to avoid None?
        
        sale = Sale()
        
        assert isinstance(sale.billAddress, Contact),\
               "invalid billAddress"

        assert isinstance(sale.shipAddress, Contact),\
               "invalid shipAddress"

        assert isinstance(sale.card, zikeshop.Card), \
               "invalid card"

        assert isinstance(sale.customer, Contact), \
               "invalid customer"
        
