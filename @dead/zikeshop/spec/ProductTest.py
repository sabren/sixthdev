
import unittest
import zikeshop

class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("delete from shop_product")
        self.cur.execute("delete from shop_product_node")
        self.cur.execute("insert into shop_product (code, name) values " + \
                         "('some01', 'something')")

    def check_nodeIDs(self):
        prod = zikeshop.Product()
        prod.code = 'some02'
        prod.name = 'something else'
        prod.nodeIDs = (1, 2, 3, 4)
        prod.save()

        self.cur.execute("select nodeID from shop_product_node where productID=2 " +\
                         "order by nodeID")

        assert self.cur.fetchall() == [(1,),(2,),(3,),(4,)], \
               "Product doesn't save nodeIDs properly"

        assert prod.nodeIDs == (1, 2, 3, 4), \
               "Product doesn't return nodeIDs properly"

        
        ## make sure it still works after an update:

        prod.nodeIDs = (1, 2)
        prod.save()
        
        self.cur.execute("select nodeID from shop_product_node where productID=2 " +\
                         "order by nodeID")

        assert self.cur.fetchall() == [(1,),(2,)], \
               "Product doesn't update nodeIDs properly"

        assert prod.nodeIDs == (1, 2), \
               "Product doesn't return nodeIDs properly after an update"

