"""
test cases for zikeshop.Store
"""
__ver__ = "$Id$"

import unittest
import zdc
import zikeshop
from zikeshop import Contact
from zikeshop import State
from zikeshop import Store
from zikeshop.test import clerk
from zikeshop.test import dbc

class StoreTestCase(unittest.TestCase):

    def setUp(self):
        self.store = Store(clerk)
        try:
            try:
                state = clerk.load(State, CD="CA")
            except:
                state = clerk.new(State)
                state.CD = "CA"
            import zdc
            state.salestax = zdc.FixedPoint("8.25")
            state.save()
        except:
            pass


    def check_salesTax(self):

        addr = clerk.new(Contact)
        addr.stateCD = 'NY'
        addr.postal = '123456'

        actual = self.store.calcSalesTax(addr, 10)
        assert actual == 0, \
               "shouldn't have sales tax because no nexus in NY"

        addr = clerk.new(Contact)
        addr.stateCD = 'CA'

        actual = self.store.calcSalesTax(addr, 10)
        goal = (zdc.FixedPoint(clerk.load(State, CD="CA").salestax)
                * 10) / 100.0
        assert actual == goal, \
               "wrong sales tax after nexus established: %s vs %s" \
               % (actual, goal)
        

    def check_products(self):
        import zikeshop.test
        cur = zikeshop.test.dbc.cursor()
        cur.execute("DELETE FROM shop_product")
        cur.execute("INSERT INTO shop_product (class, name)" 
                    "values ('product', 'asdfasf')")
        actual = len(self.store.products)
        assert actual==1, \
               "wrong # of products found: %s"  % actual
        

    def check_fakedata(self):
        import fakedata
        fakedata.load()
