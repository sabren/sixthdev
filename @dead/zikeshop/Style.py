"""
Style object for managing product styles...

$Id$
"""

import zdc
import zikeshop

class Style(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_style")
    _defaults = {}
    _tuples = []


    def get_product(self):
        return zikeshop.Product(ID=self.productID)

    def __str__(self):
        return "%s [%s]" % (self.product.name, self.style)
