"""
test cases for zikeshop.Store
"""
__ver__ = "$Id$"

import unittest
import zikeshop

class StoreTestCase(unittest.TestCase):

    def setUp(self):
        self.store = zikeshop.Store()

    def check_salesTax(self):

        self.store.address = zikeshop.Address()
        self.store.address.stateCD = 'TX'
        
        addr = zikeshop.Address()
        addr.stateCD = 'CA'
        addr.postal = '90210'

        actual = self.store.calcSalesTax(addr, 10)
        assert actual == 0, \
               "shouldn't have sales tax because no nexus in CA"

        newaddr = zikeshop.Address()
        newaddr.stateCD = 'CA'
        newaddr.postal = '90210'
        #self.store.addLocation(newaddr)
        self.store.address = newaddr
        actual = self.store.calcSalesTax(addr, 10)
        goal = (zikeshop.State(CD="CA").salestax * 10) / 100
        assert actual == goal, \
               "wrong sales tax after nexus established: %s vs %s" \
               % (actual, goal)
        

    def tearDown(self):
        self.store.delete()
