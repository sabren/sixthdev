"""
Style object for managing product styles...
"""
__ver__="$Id$"

import zdc
import zikeshop

class Style(zikeshop.Product):
    __super = zikeshop.Product

    def _new(self):
        self.__super._new(self)
        self._data['class'] = "style"
    
    def get_product(self):
        if self.parentID:
            return zikeshop.Product(ID=self.parentID)
        else:
            return None

    def get_label(self):
        return "%s [%s]" % (self.product.name, self.name)
