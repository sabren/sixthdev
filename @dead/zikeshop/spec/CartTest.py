"""
testCart.py - test for zikeshop.Cart object

$Id$
"""

import unittest
import zikeshop

class CartTestCase(unittest.TestCase):

    def setUp(self):
        self.cart = zikeshop.Cart(pool={})


    def check_isEmpty(self):
        assert self.cart.isEmpty(), \
               "Cart should be empty by default."

        self.cart.add("frogs")
        assert not self.cart.isEmpty(), \
               "Cart shouldn't be empty when there's stuff in it."


    def check__getKey(self):
        assert self.cart._getKey() == "__cart_", \
               "doesn't return the expected key."        

        cart = zikeshop.Cart(pool={}, name="elvis")
        assert cart._getKey() == "__cart_elvis", \
               "doesn't properly encode the cart name in the key"


    def check_q_contents(self):
        assert self.cart.q_contents() == [], \
               "q_contents returns wrong thing with empty cart"

        self.cart.add("fried green tomatoes", 1.25, 2)
        self.cart.add("red hot chili peppers")
        goal = [
            {"label":"fried green tomatoes", "extra":None,
             "price": 1.25, "quantity":2, "link":"" },
            {"label":"red hot chili peppers", "extra":None,
             "price":0, "quantity":1, "link":"" }]

        assert self.cart.q_contents() == goal, \
               "q_contents returns wrong thing with full cart"
        

    def check_add(self):
        self.cart.add("bananas")
        goal = [{"label":"bananas", "price":0,
                 "link":"", "quantity":1, "extra":None},]
        assert self.cart.q_contents() == goal, \
               "doesn't have the correct contents"


    def check_update(self):
        self.cart.add("something")
        self.cart.add("something", quantity=2)
        self.cart.add("something", quantity=1)

        self.cart.update(0, 2)
        assert self.cart.q_contents()[0]["quantity"] == 2, \
               "update doesn't set the right quantities"
        
        
        self.cart.update(0, None)
        assert self.cart.q_contents()[0]["quantity"] == 2, \
               "update screws up quantities when newQuantity is None"
        

    def check_remove(self):
        self.cart.add("something")
        self.cart.remove(0)

        assert self.cart.isEmpty(), \
               "cart.remove(item) doesn't work"
        
    
    def check_purge(self):
        self.cart.add("cheese")
        self.cart.update(0, 0)
        self.cart.purge()
        
        assert self.cart.isEmpty(), \
               "cart.purge() doesn't purge items"


    def check_subtotal(self):
        self.cart.add("fried green tomatoes", 1.25, 2)
        self.cart.add("red hot chili peppers", 2.5, 5)

        assert self.cart.subtotal()==15, \
               "cart.subtotal screwed up. expected 15, got: %s" \
               % self.cart.subtotal()


    def tearDown(self):
        del self.cart

