"""
zikeshop!
"""
__ver__="$Id$"

import zikeshop
zikeshop.siteID = 1 # @TODO: get rid of this

class ShopApp(zikeshop.PublicApp):
    __super = zikeshop.PublicApp

    def enter(self):
        self.__super.enter(self)
        # grab functions that define urls for the system:
        self.consult("lib_link")
        

    def fetch_class(self, what):
        if what=="category":
            return zikeshop.Category
        elif what=="product":
            return zikeshop.Product

    def act_(self):
        self.do("show", what="category")


    def show_category(self):
        import zikeshop, zdc, zebra
        if self.input.get("path","/")== "/":
            cat = zikeshop.Category()
            cat.ID = 0
        else:
            cat = zikeshop.Category(path=self.input["path"])

        self.consult(zdc.ObjectView(cat))
        zebra.show("dsp_category", self.model)

    def show_product(self):
        import zikeshop, zdc, zebra
        prod = zikeshop.Product(code=self.input["code"])
        self.consult(zdc.ObjectView(prod))
        zebra.show("dsp_product", self.model)


if __name__=="__main__":
    ShopApp().act()

