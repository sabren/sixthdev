
import unittest
import weblib
import zikebase
import zikeshop.test

import sys
sys.path.append('admin/')

class AdminPagesTestCase(unittest.TestCase):

    def setUp(self):
        if hasattr(weblib, "auth"): del weblib.auth
        if hasattr(weblib, "request"): del weblib.request

        #weblib.auth = zikebase.UserAuth()
        import zike
        weblib.auth = zike.ZikeAuth() # because of siteID
        
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("delete from shop_product")
        self.cur.execute("delete from base_node")
        self.qStr = "auth_check_flag=1&auth_username=username"\
                    "&auth_password=password"

        from zikebase import md5crypt
        self.cur.execute("DELETE FROM base_user")
        self.cur.execute("INSERT INTO base_user (username,cryptedpass,siteID)"
                         "VALUES ('username', '%s', 1)" \
                         % md5crypt.md5crypt("password", "pw"))




    def check_Pages(self):
        """just check that the pages all come up..."""

        for page in [
            "e_category.py",
            #"e_inventory.py", # it expects a productID
            "e_location.py",
            "e_product.py",
            "e_style.py",

            "l_category.py",
            "l_location.py",
            "l_product.py",
            "v_product.py",
            ]:
            eng = weblib.Engine(script=open("admin/" + page))
            eng.run()

            if eng.result != eng.SUCCESS:
                print eng.error
            
            assert eng.result == eng.SUCCESS, \
                   "The %s script broke!" % page


    def check_ProductAdd(self):

        eng = weblib.Engine(script=open('admin/e_product.py'),
                            request=weblib.Request(querystring=self.qStr,
                                                   form=
                                                   {"action": "save",
                                                    "code": "XY001",
                                                    "name": "Xylaphone",
                                                    "descriptLong":
                                                             "makes music"}
                                                   ))
        eng.run()
        self.cur.execute("SELECT code, name, descriptLong " \
                         "FROM shop_product WHERE ID=1")

        assert self.cur.fetchone() == ("XY001", "Xylaphone", "makes music"), \
               "Product admin page doesn't add products!!"
        


    def check_ProductEdit(self):
        self.cur.execute("insert into shop_product (code) values ('SADFASDF')")
        
        eng = weblib.Engine(script=open('admin/e_product.py'),
                            request=weblib.Request(querystring=self.qStr,
                                                   form = \
                                                   {"action": "save",
                                                    "ID" : 1,
                                                    "code": "XY001",
                                                    "name": "Xylaphone",
                                                    "nodeIDs": ("1","2"),
                                                    "descriptLong":
                                                          "makes music" }))
        eng.run()

        assert eng.result == eng.SUCCESS, \
               "got error trying to update product:\n%s" \
               % eng.error
        
        self.cur.execute("SELECT code, name, descriptLong "\
                         "FROM shop_product WHERE ID=1")
        assert self.cur.fetchone() == ("XY001", "Xylaphone", "makes music"), \
               "Product admin page doesn't update products correctly!!"

        self.cur.execute("SELECT nodeID FROM shop_product_node "\
                         "WHERE productID=1")
        assert self.cur.rowcount == 2, \
               "Product admin doesn't put products in nodes correctly"



    def check_NodeAdd(self):
        eng = weblib.Engine(script=open('admin/e_category.py'),
                            request=weblib.Request(querystring=self.qStr,
                                                   form = \
                                                   {"action": "save",
                                                    "name": "My Node",
                                                    "parentID": "0",
                                                    "descript":
                                                          "just a node" }))
        eng.run()
        assert eng.result == eng.SUCCESS, \
               "Trouble running e_category.py:\n%s" % eng.error
        
        self.cur.execute("SELECT name, parentID, descript, path " + \
                         "FROM base_node WHERE ID=1")
        goal = ("My Node", 0, "just a node", "My Node")
        actual = self.cur.fetchone()

        assert actual == goal, \
               "Node admin page creadted bad node: %s" % actual
