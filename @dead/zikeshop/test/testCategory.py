"""
tests for zikeshop.Category

$Id$
"""

import unittest
import zikeshop

class CategoryTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()


    def check_q_products(self):
        self.cur.execute("DELETE FROM base_node")
        self.cur.execute("DELETE FROM shop_product")
        self.cur.execute("DELETE FROM shop_product_node")
        self.cur.execute("INSERT INTO base_node (name) values ('whatever')")
        self.cur.execute("INSERT INTO shop_product (code, name, siteID) "
                         "VALUES ('a', 'ant', 1)")
        self.cur.execute("INSERT INTO shop_product (code, name, siteID) "
                         "VALUES ('b', 'box', 1)")
        self.cur.execute("INSERT INTO shop_product (code, name, siteID) "
                         "VALUES ('c', 'car', 2)")
        self.cur.execute("INSERT INTO shop_product_node (productID, nodeID) "
                         "VALUES (1, 1)")
        self.cur.execute("INSERT INTO shop_product_node (productID, nodeID) "
                         "VALUES (2, 1)")
        self.cur.execute("INSERT INTO shop_product_node (productID, nodeID) "
                         "VALUES (3, 1)")

        zikeshop.siteID = 1
        prods = zikeshop.Category(ID=1).q_products()
        assert len(prods) == 2, \
               "wrong number of categories (%s) shown on category page" \
               % len(prods)


        zikeshop.siteID = 2
        prods = zikeshop.Category(ID=1).q_products()
        assert len(prods) == 1, \
               "wrong number of categories (%s) shown on category page" \
               % len(prods)


