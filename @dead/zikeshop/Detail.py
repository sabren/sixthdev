"""
An Event Detail.
"""
__ver__="$Id$"

import zdc
import zikeshop

class Detail(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_detail")
    _tuples = ["product"]

    def _new(self):
        self.__super._new(self)
        self.saleID = 0
        self.productID = 0
        self.quantity = 0
        self.subtotal = 0

    def get_product(self):
        return zikeshop.Product(ID=self.productID)

