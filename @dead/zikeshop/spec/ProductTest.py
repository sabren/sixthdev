
import unittest
import zikeshop

class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("delete from shop_product")
        self.cur.execute("delete from shop_product_node")
        self.cur.execute("insert into shop_product (code, product) values " + \
                         "('some01', 'something')")

    def check_nodeIDs(self):
        prod = zikeshop.Product(ID=1)
        prod.nodeIDs = (1, 2, 3, 4)

        self.cur.execute("select nodeID from shop_product_node where productID=1 " +\
                         "order by nodeID")

        assert self.cur.fetchall() == [(1,),(2,),(3,),(4,)], \
               "Product doesn't save nodeIDs properly"


        assert prod.nodeIDs == (1, 2, 3, 4), \
               "Product doesn't return nodeIDs properly"


