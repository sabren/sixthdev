"""
testCart.py - test for zikeshop.Cart object

$Id$
"""

import unittest
import zikeshop

class CartTest(unittest.TestCase):

    def setUp(self):
        self.cart = zikeshop.Cart({})


    def test_isEmpty(self):
        assert self.cart.isEmpty(), \
               "Cart should be empty by default."

        self.cart.add("frogs")
        assert not self.cart.isEmpty(), \
               "Cart shouldn't be empty when there's stuff in it."


    def test__getKey(self):
        assert self.cart._getKey() == "__cart_", \
               "doesn't return the expected key."        

        cart = zikeshop.Cart({}, name="elvis")
        assert cart._getKey() == "__cart_elvis", \
               "doesn't properly encode the cart name in the key"


    def test_q_contents(self):
        assert self.cart.q_contents() == [], \
               "q_contents returns wrong thing with empty cart"

        self.cart.add("fried green tomatoes", 1.25, 2)
        self.cart.add("red hot chili peppers")
        goal = [
            {"label":"fried green tomatoes", "extra":None,
             "price": 1.25, "quantity":2, "link":"" },
            {"label":"red hot chili peppers", "extra":None,
             "price":0, "quantity":1, "link":"" }]

        actual = self.cart.q_contents()
        for row in range(len(goal)):
            for item in goal[row].keys():
                assert actual[row][item] == goal[row][item], \
                       "q_contents returns wrong thing with full cart"
        

    def test_add(self):
        self.cart.add("bananas")
        goal = {"label":"bananas", "price":0,
                "link":"", "quantity":1, "extra":None}
        contents = self.cart.q_contents()
        assert len(contents) == 1, \
               "wrong content length. expected 1, got: %i" % len(contents)
        for item in goal.keys():
            assert contents[0][item] == goal[item], \
                   "wrong contents attribute: %s" % item


    def test_update(self):
        self.cart.add("something")
        self.cart.add("something", quantity=2)
        self.cart.add("something", quantity=1)

        self.cart.update(0, 2)
        assert self.cart.q_contents()[0]["quantity"] == 2, \
               "update doesn't set the right quantities"
        
        
        self.cart.update(0, None)
        assert self.cart.q_contents()[0]["quantity"] == 2, \
               "update screws up quantities when newQuantity is None"
        

    def test_remove(self):
        self.cart.add("something")
        self.cart.remove(0)

        assert self.cart.isEmpty(), \
               "cart.remove(item) doesn't work"
        
    
    def test_purge(self):
        self.cart.add("cheese")
        self.cart.update(0, 0)
        self.cart.purge()
        
        assert self.cart.isEmpty(), \
               "cart.purge() doesn't purge items"


    def test_subtotal(self):
        self.cart.add("fried green tomatoes", 1.25, 2)
        self.cart.add("red hot chili peppers", 2.5, 5)

        assert self.cart.subtotal()==15, \
               "cart.subtotal screwed up. expected 15, got: %s" \
               % self.cart.subtotal()


    def test_calcWeight(self):
        self.cart.add("2 tens", 1, 2, extra={"weight":10})
        self.cart.add("3 ones", 1, 3, extra={"weight":1})
        actual = self.cart.calcWeight()
        assert actual == 23, \
               "calcWeight() returns wrong value: %s" % actual

    def tearDown(self):
        del self.cart

if __name__=="__main__":
    unittest.main()
    
