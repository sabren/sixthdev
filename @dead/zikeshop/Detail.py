"""
a Sale Detail.
"""
__ver__="$Id$"

from strongbox import *
from zikeshop import Style
from zikeshop import Product

class Detail(Strongbox):
    ID = attr(long)
    product = link(Product) #@TODO: this might be a style!?
    productID = attr(long, default=0)  #@TODO: kill this?
    saleID = attr(long, default=0)
    quantity = attr(long, default=0)

    ### subtotal calculation #######################################
    def get_subtotal(self):
        if self.product:
            return self.product.price * self.quantity
        else:
            return 0
        
    def set_subtotal(self, value):
        raise TypeError, "subtotal is read-only."
        
    #@TODO: auto-calculate subtotal field for saving to database
    
