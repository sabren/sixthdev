"""
test cases for zikeshop.Store
"""
__ver__ = "$Id$"

import unittest
import zikeshop, zikebase

class StoreTestCase(unittest.TestCase):

    def setUp(self):
        self.store = zikeshop.Store()

    def check_address(self):
        assert isinstance(self.store.address, zikebase.Contact), \
               "Invalid address: %s" % self.store.address
        

    def check_salesTax(self):

        self.store.address = zikebase.Contact()
        self.store.address.stateCD = 'TX'
        
        addr = zikebase.Contact()
        addr.stateCD = 'CA'
        addr.postal = '90210'

        actual = self.store.calcSalesTax(addr, 10)
        assert actual == 0, \
               "shouldn't have sales tax because no nexus in CA"

        newaddr = zikebase.Contact()
        newaddr.stateCD = 'CA'
        newaddr.postal = '90210'
        self.store.address = newaddr
        actual = self.store.calcSalesTax(addr, 10)
        goal = (zikeshop.State(CD="CA").salestax * 10) / 100
        assert actual == goal, \
               "wrong sales tax after nexus established: %s vs %s" \
               % (actual, goal)
        

    def check_fakedata(self):
        import fakedata
        fakedata.load()

    def tearDown(self):
        self.store.delete()
