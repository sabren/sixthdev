"""
Cart app for zikeshop.
"""

import zikeshop

class CartApp(zikeshop.PublicApp):
    __super = zikeshop.PublicApp

    def __init__(self, cart, ds, input=None):
        self.__super.__init__(self, cart, ds, input)
        self.silent = 0
        self.consult("lib_link")

    def act_(self):
        self.do("view")

    def act_add(self):

        productID = self.input.get("productID")
        assert productID, "Don't know what to add."

        prod = zikeshop.Product(self.ds, ID=productID)
        #@TODO: FIX THIS HORRIBLE MESS:
        if prod._data["class"] == "style":
            style = zikeshop.Style(self.ds, ID=productID)
            label = str(style)
        else:
            label = str(prod)
        
        if prod._data["class"] == "product":
            link = "shop.py?action=show_product&code=%s" \
                   % prod.code
        else:
            # it's a style:
            link  = "shop.py?action=show_product&code=%s" \
                    % (style.product.code)

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
    CartApp(zikeshop.Cart(sess), ds).act()
    sess.stop()
