
import unittest
import weblib
import zikeshop.test

import sys
sys.path.append('admin/')

class AdminPagesTestCase(unittest.TestCase):

    def setUp(self):
        self.cur = zikeshop.test.dbc.cursor()
        self.cur.execute("delete from shop_product")
        self.cur.execute("delete from base_node")


    def check_Pages(self):
        """just check that the pages all come up..."""

        for page in ["adm_product.py", "adm_node.py"]:
            eng = weblib.Engine(script=open("admin/" + page))
            eng.run()
            
            assert eng.result == eng.SUCCESS, \
                   "The %s script broke!" % page


    def check_ProductAdd(self):
        eng = weblib.Engine(script=open('admin/adm_product.py'),
                            request=weblib.Request(form = \
                                                   {"action": "save",
                                                    "code": "XY001",
                                                    "name": "Xylaphone",
                                                    "descriptLong": "makes music" }))
        eng.run()
        self.cur.execute("select code, name, descriptLong from shop_product where ID=1")

        assert self.cur.fetchone() == ("XY001", "Xylaphone", "makes music"), \
               "Product admin page doesn't add products!!"
        


    def check_ProductEdit(self):
        self.cur.execute("insert into shop_product (code) values ('SADFASDF')")
        
        eng = weblib.Engine(script=open('admin/adm_product.py'),
                            request=weblib.Request(form = \
                                                   {"action": "save",
                                                    "ID" : 1,
                                                    "code": "XY001",
                                                    "name": "Xylaphone",
                                                    "descriptLong": "makes music" }))
        eng.run()
        self.cur.execute("select code, name, descriptLong from shop_product where ID=1")
        
        assert self.cur.fetchone() == ("XY001", "Xylaphone", "makes music"), \
               "Product admin page doesn't update products correctly!!"
        




    def check_NodeAdd(self):
        eng = weblib.Engine(script=open('admin/adm_node.py'),
                            request=weblib.Request(form = \
                                                   {"action": "save",
                                                    "name": "My Node",
                                                    "parentID": "0",
                                                    "descript": "just a node" }))
        eng.run()

        self.cur.execute("SELECT name, parentID, descript, path " + \
                         "FROM base_node WHERE ID=1")

        assert self.cur.fetchone() == ("My Node", 0, "just a node", "My Node"), \
               "Node admin page doesn't add nodes!!"
        
