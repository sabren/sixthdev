"""
test routines for the Cashier class

$Id$
"""

import unittest
import zikeshop

class CashierTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("DELETE FROM shop_sale")
        self.cur.execute("DELETE FROM shop_sale_item")

    def check_checkout(self):
        cart = zikeshop.Cart({})
        cart.add("apples", price=2, quantity=3, extra={"styleID":"20"})
        cart.add("bananas", price=1, quantity=2, extra={"styleID":"30"})
        cart.add("oranges", price=1, quantity=1, extra={"styleID":"50"})
        
        input = {"action":"checkout"}
        sess = {}
        cust = zikeshop.Customer(ID=1)
        cash = zikeshop.Cashier(cart, cust, input, pool=sess)

        cash.shipAddressID = 1
        cash.billAddressID = 1
        cash.cardID = 1

        cash.act_checkout()

        assert cart.isEmpty(), \
               "Cashier doesn't empty cart after checkout."

        for item in cash.storedFields:
            assert getattr(cash, item) is None, \
                   "Cashier doesn't forget %s after checkout." % item

        self.cur.execute("SELECT ID, statusID, subtotal FROM shop_sale")
        assert self.cur.rowcount==1, \
               "Expected 1 sale after checkout, got %i." % self.cur.rowcount

        row = self.cur.fetchone()
        saleID = row[0]

        assert row[2]=="9.00", \
               "expected subtotal of 9, got %s" % row[2]
        

        status = zikeshop.Status(ID=row[1]).status
        assert status=='new', \
               "expected 'new' status, got: %s" % status

        self.cur.execute("SELECT styleID, item FROM shop_sale_item "
                         "WHERE saleID=%i ORDER BY item" % saleID)
        assert self.cur.rowcount==3, \
               "Expected 3 sold items, got %i." % self.cur.rowcount

        row = self.cur.fetchone()
        assert row == (20, "apples"), \
               "Got wrong row: %s" % str(row)


