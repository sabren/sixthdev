"""
Cart app for zikeshop.
"""

import zikeshop

class CartApp(zikeshop.PublicApp):
    __super = zikeshop.PublicApp

    def __init__(self):
        self.__super.__init__(self)
        self.silent = 0
        self.consult("lib_link")

    def act_(self):
        self.do("view")

    def act_add(self):

        productID = self.input.get("productID")
        assert productID, "Don't know what to add."

        prod = zikeshop.Product(ID=productID)

        label = prod.name
        link  = "product/%s" % (prod.code)

        extra={"ID":prod.ID, "weight": prod.weight}
        quantity = self.input.get("quantity")

        self.cart.add(label, prod.price, quantity, link, extra)
        self.next = "view"

    def act_view(self):
        import zebra
        self.model["contents"] = self.cart.q_contents()
        self.model["total"] = self.cart.subtotal()
        if not self.silent:
            zebra.show("dsp_cart", self.model)


    def act_remove(self):
        items = []
        for i in range(self.cart.count()):
            if self.input.get("remove_%s" % i):
                self.cart.update(i, 0)
        self.cart.purge()
        self.do("view")
        

    def act_update(self):
        quantities = []
        for i in range(self.cart.count()):
            try:
                newamt = int(self.input.get("quantity_%s" % i, 0))
            except:
                newamt = 0
            self.cart.update(i, newamt)
        self.do("view")


if __name__=="__main__":
    CartApp().act()
