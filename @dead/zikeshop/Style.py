"""
Style object for managing product styles...
"""
__ver__="$Id$"

import zdc
import zikeshop

class Style(zikeshop.Product):
    __super = zikeshop.Product

    #@TODO: inherit defaults, but still override?
    _defaults = {
        "class":"style",
        "price": 0,
        "retail": 0,
        "weight": 0,
        "parentID": 0,
        "inStock": 0,
        "onHold" : 0,
        }

    
    def get_product(self):
        if self.parentID:
            return zikeshop.Product(ID=self.parentID)
        else:
            return None

    def __str__(self):
        return "%s [%s]" % (self.product.name, self.style)
