import unittest
import zikeshop
from pytypes import FixedPoint
from zikeshop import Contact
from zikeshop import State
from zikeshop import Store
from zikeshop.test import clerk
from zikeshop.test import dbc

class StoreTestCase(unittest.TestCase):
    __ver__ = "$Id$"

    def setUp(self):
        self.store = Store(clerk)
        try:
            try:
                state = clerk.match(State, CD="CA")[0]
            except:
                state = State(CD="CA")
            state.salestax = FixedPoint("8.25")
            clerk.store(state)
        except:
            pass


    def check_salesTax(self):

        addr = Contact()
        addr.stateCD = 'NY'
        addr.postal = '123456'

        actual = self.store.calcSalesTax(addr, 10)
        assert actual == 0, \
               "shouldn't have sales tax because no nexus in NY"

        addr = Contact()
        addr.stateCD = 'CA'

        actual = self.store.calcSalesTax(addr, 10)
        goal = (FixedPoint(clerk.match(State, CD="CA")[0].salestax)
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
