"""
test code for the Bagger class
"""
__ver__="$Id$"

import weblib
import zikeshop
import unittest

class BaggerTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        pass


    def check_input(self):
        bagr = zikeshop.Bagger(zikeshop.Cart({}), {"MY":"INPUT"})
        assert bagr.input == {"MY":"INPUT"}, \
               "bagger doesn't rememeber its input"

        weblib.request = {"B":"C"}
        bagr = zikeshop.Bagger(zikeshop.Cart({}))
        assert bagr.input == {"B":"C"},\
               "bagger shold use weblib.request as input"
        del weblib.request

        
    def check_add(self):
        import zikeshop; zikeshop.siteID = 1
        self.cur.execute("DELETE FROM shop_product")
        self.cur.execute("DELETE FROM shop_style")
        self.cur.execute("INSERT INTO shop_product (name, code, price,siteID) "
                         "VALUES ('apple', 'APPL', 4.25, 1)")
        self.cur.execute("INSERT INTO shop_style (productID, style) "
                         "VALUES (1, 'green')")
        self.cur.execute("INSERT INTO shop_style (productID, style) "
                         "VALUES (1, 'red')")
        
        bagr = zikeshop.Bagger(zikeshop.Cart({}), {"styleID":1})
        bagr.act("add")

        contents = bagr.cart.q_contents()

        assert len(contents) == 1,\
               "bagger.cart.q_contents() has wrong length"

        item = contents[0]
        assert item["label"] == "apple [green]",\
               "bagger set wrong label (%s)" % item["label"]
        assert item["quantity"] == 1,\
               "bagger set wrong quantity (%s)" % item["quantity"]
        assert item["price"] == zikeshop.FixedPoint("4.25"), \
               "bagger set wrong price (%s)"  % item["price"]
        assert item["link"] == "product/APPL",\
               "bagger set wrong link (%s)" % item["link"]
        assert item["extra"]["styleID"]==1,\
               "bagger set wrong extra (%s)" % item["extra"]
        
    

    def check_update(self):
        cart = zikeshop.Cart({})
        cart.add("superman")
        cart.add("batman")
        cart.add("spiderman")
        cart.add("cartman")

        bagr = zikeshop.Bagger(cart, {"action":"update",
                                      "quantity_0":1,
                                      "quantity_1":2,
                                      "quantity_2":3,
                                      "quantity_3":4, })
        bagr.act()
        contents = cart.q_contents()
        for x in range(4):
            assert contents[x]["quantity"] == x + 1, \
                   "wrong quantity for item %s" %x
        
