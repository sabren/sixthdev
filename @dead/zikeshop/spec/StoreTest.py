import unittest
import zikeshop
from pytypes import FixedPoint
from zikeshop import Contact
from zikeshop import State
from zikeshop import Store

from arlo import MockClerk
clerk = MockClerk()

#@TODO: is store anything more than a clerk?

class StoreTest(unittest.TestCase):
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


    def test_salesTax(self):

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

    def test_fakedata(self):
        import fakedata
        fakedata.load()

if __name__=="__main__":
    unittest.main()
    
