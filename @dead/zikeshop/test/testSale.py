"""
test cases for zikeshop.Sale
"""
__ver__ = "$Id$"

import unittest
import zikeshop, zikebase
from zikeshop.test import dbc as ds

zikebase.load("Contact")
class SaleTestCase(unittest.TestCase):

    
    def check_links(self):
        sale = zikeshop.Sale(ds)
        
        assert isinstance(sale.billAddress, zikebase.Contact),\
               "invalid billAddress"

        assert isinstance(sale.shipAddress, zikebase.Contact),\
               "invalid shipAddress"

        assert isinstance(sale.card, zikeshop.Card), \
               "invalid card"

        assert isinstance(sale.customer, zikebase.Contact), \
               "invalid customer"
        
