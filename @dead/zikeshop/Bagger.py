"""
An actor to move Products in and out of a Cart.

$Id$
"""

import zikeshop

class Bagger(zikeshop.ShopActor):

    def act_add(self):
        styleID = self.input.get("styleID")
        assert styleID, "Don't know what to add."

        style = zikeshop.Style(ID=styleID)
        prod = style.product
        assert prod.siteID == zikeshop.siteID, \
               "Invalid product"
        

        if style.style is None:
            label = prod.name
        else:
            label = "%s [%s]" % (prod.name, style.style)
        link  = "product/%s" % (prod.code)

        extra={"styleID":style.ID, "weight": prod.weight}

        quantity = self.input.get("quantity")
        
        #@TODO: bug in zdc [or python?] preventing get_price from working.. 
        self.cart.add(label, prod.get_price(), quantity, link, extra)



    def act_remove(self):
        items = []
        for i in range(self.cart.count()):
            if self.input.get("remove_%s" % i):
                self.cart.update(i, 0)
        

    def act_update(self):
        quantities = []
        for i in range(self.cart.count()):
            try:
                newamt = int(self.input.get("quantity_%s" % i, 0))
            except:
                newamt = 0
            self.cart.update(i, newamt)



