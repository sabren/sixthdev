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
        addr = zikeshop.Address()
        addr.stateCD = 'CA'
        addr.postal = '90210'

        actual = self.store.calcSalesTax(addr, 10)
        assert actual == 0, \
               "shouldn't have sales tax because no nexus in CA"

        newaddr = zikeshop.Address()
        newaddr.stateCD = 'CA'
        newaddr.postal = '90210'
        self.store.addLocation(newaddr)
        actual = self.store.calcSalesTax(addr, 10)
        goal = (zikeshop.State(CD="CA").salestax * 10) / 100
        assert actual == goal, \
               "wrong sales tax after nexus established: %s vs %s" \
               % (actual, goal)
        

    def check_inventory(self):
        prod1 = zikeshop.Product()
        prod2 = zikeshop.Product()

        loc1 = zikeshop.Location()
        loc1.incInventory(prod1, 10)
        loc1.incInventory(prod1, 20) # leaving 30
        loc1.incInventory(prod2, 5)  

        loc2 = zikeshop.Location()
        loc2.incInventory(prod1, 15)
        loc2.incInventory(prod2, 15)
        loc2.decInventory(prod1, 5)  # leaving 10

        self.store.addLocation(loc1)
        self.store.addLocation(loc2)

        goal = 40
        actual = self.store.calcInventory(prod1)
        assert actual  == goal, \
               "store.inventory doesn't work. (%s vs %s)" \
               % (actual, goal)

        self.store.hold(prod1, 1)
        goal = 39
        actual = self.store.calcAvailable(prod1)
        assert actual == goal, \
               "store.calcAvailable doesn't work (%s vs %s)" \
               % (actual, goal)
        

    def check_shipping(self):
        raise "no shipping tests yet"

    def check_shippingee(self):
        raise "turn admin and public page tests back on"


    def tearDown(self):
        self.store.delete()
