"""
zikeshop!
"""
__ver__="$Id$"

import zikeshop
from zikeshop import Cart
from zikeshop import Category
from zikeshop import Product
from zikeshop import PublicApp

class ShopApp(zikeshop.PublicApp):
    __super = zikeshop.PublicApp

    def enter(self):
        self.__super.enter(self)
        # grab functions that define urls for the system:
        self.consult("lib_link")
        
    def act_(self):
        self.do("show_category")


    def act_show_category(self):
        import zdc, zebra
        if self.input.get("path","/")== "/":
            cat = self.clerk.new(Category)
            cat.ID = 0
        else:
            cat = self.clerk.load(Category, path=self.input["path"])

        self.consult(zdc.ObjectView(cat))
        self.write(zebra.fetch("dsp_category", self.model))

    def act_show_product(self):
        import zdc, zebra
        prod = self.clerk.load(Product, code=self.input["code"])
        self.consult(zdc.ObjectView(prod))
        print >> self, zebra.fetch("dsp_product", self.model)


if __name__=="__main__":
    print >> RES, ShopApp(REQ, Cart(SESS), DBC).act()
