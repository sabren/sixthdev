"""
A Node with Products in it.
"""
__ver__="$Id$"

import zikeshop, zdc, zikebase
zikebase.load("Node")

class Category(zikebase.Node):
    __super = zikebase.Node
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
        self.__super.delete(self)
