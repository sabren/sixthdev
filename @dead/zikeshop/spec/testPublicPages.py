
import unittest
import weblib; reload(weblib) # or else it'll break tests.. but why?
import zikeshop.test

import sys
sys.path.append('public/')
zikeshop.basehref = ''


class PublicPagesTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        weblib.auth = zikeshop.CustomerAuth()

    def check_Pages(self):
        """just check that the pages all come up..."""

        for page in [
            "cart.py",
            "category.py",
            "checkout.py",
            #"product.py", # requires a product code
            ]:

            eng = weblib.Engine(script=open("public/" + page))
            eng.run()

            if eng.result != eng.SUCCESS:
                print eng.error
            
            assert eng.result == eng.SUCCESS, \
                   "The %s script broke!" % page




    def check_category(self):
        import zikeshop
        zikeshop.siteID = 1

        self.cur.execute("DELETE FROM base_node")
        self.cur.execute("DELETE FROM shop_product")
        self.cur.execute("DELETE FROM shop_product_node")
        self.cur.execute("INSERT INTO base_node (name, path, siteID) "
                         "VALUES ('whatever', 'whatever' ,1)")
        self.cur.execute("INSERT INTO base_node (name ,siteID, parentID) "
                         "VALUES ('childnode',1, 1)")
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
        
        eng=weblib.Engine(request=weblib.Request(querystring="path=whatever"),
                          script=open("public/category.py"))
        eng.run()

        assert eng.result == eng.SUCCESS, \
               "the category script broke: \n%s" % eng.error

        assert len(eng.locals["model"].products) == 2, \
               "wrong number of products (%s) shown on category page" \
               % eng.locals["model"].products

        assert len(eng.locals["model"].children) == 1, \
               "wrong number of children (%s) shown on category page" \
               % eng.locals["model"].children



    def check_newcustomer(self):
        import zikeshop; zikeshop.siteID = 1

        self.cur.execute("DELETE FROM base_user")

        req = weblib.Request(form={
            "action":"save",
            "email":"fred@tempy.com",
            "password":"rufus",
            })
        eng = weblib.Engine(script=open("public/newcustomer.py"),
                            request=req)

        eng.run()

        assert eng.result == eng.SUCCESS, \
               "trouble with newcustomer.py:\n %s" % eng.error

        try:
            fred = zikeshop.Customer(ID=1)
        except:
            assert 0, "Oh my god! They killed Fred. You bastards!"

        assert fred.siteID == 1, \
               "fred got stuck in the wrong site"
        assert len(fred.uid) == 32, \
               "fred doesn't feel special, because his uid was: %s" % fred.uid
        assert fred.email == 'fred@tempy.com', \
               "didn't get fred's email address."

        assert fred.password == "rufus", \
               "fred has wrong password"

        addr = fred.address

