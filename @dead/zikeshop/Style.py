"""
Style object for managing product styles...
"""
__ver__="$Id$"

import zdc
import zikeshop

class Style(zikeshop.Product):

    def _new(self):
        super(Style,self)._new()
        self._data['class'] = "style"
    
    def get_product(self):
        if self.parentID:
            return zikeshop.Product(self._ds, ID=self.parentID)
        else:
            return None

    def get_label(self):
        return "%s [%s]" % (self.product.name, self.name)
