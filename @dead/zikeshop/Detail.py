"""
a Sale Detail.
"""
__ver__="$Id$"

import zdc
import zikeshop

class Detail(zdc.RecordObject):
    __super = zdc.RecordObject
    _tablename = "shop_detail"
    _tuples = ["product"]

    def _new(self):
        self.__super._new(self)
        self.saleID = 0
        self.productID = 0
        self.quantity = 0

    # @TODO: this won't (?) save products that have no ID when saved?
    # (but that only happens when testing, right?)
    # the best bet is to make this into a zdc.link of some kind..
    def set_product(self, value):
        self.productID = value.ID
        self._data['_prod'] = value

    def get_product(self):
        res = None
        if  hasattr(self, "_prod"):
            return self._prod
        elif self.productID:
            #@TODO: this is a HORRIBLE way to do this:
            res = zikeshop.Product(self._ds, ID=self.productID)
            if res._data["class"]=="style":
                res = zikeshop.Style(self._ds, ID=self.productID)
        return res

    ### subtotal calculation #######################################
    def get_subtotal(self):
        if self.product:
            return self.product.price * self.quantity
        else:
            return 0
        
    def set_subtotal(self, value):
        raise TypeError, "subtotal is read-only."
        
    def save(self):
        # add the calculated field to the actual record:
        self._data["subtotal"] = self.subtotal
        self.__super.save(self)
