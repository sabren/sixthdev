"""
A Node with Products in it.
"""
__ver__="$Id$"

import sixthday
import zikeshop
import zdc


class Category(sixthday.Node):
    _tuples = ["crumbs", "children", "products"] # @TODO: clean this up!

    def get_products(self):
        if not self._data.has_key("prods"):
            self._data["prods"] = zdc.Junction(self,
                                               zikeshop.Product,
                                               "shop_product_node",
                                               "nodeID", "productID")
            self._data["prods"].fetch()
        return self._data["prods"]

    def delete(self):
        assert len(self.products)==0, \
               "Cannot delete a category that has products in it."
        super(Category,self).delete()
