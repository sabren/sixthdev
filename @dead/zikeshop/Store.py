"""
class to represent the actual store
"""
__ver__="$Id$"

import zdc
import zikeshop

class Store(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_store")

    def get_address(self):
        return zikeshop.Address(ID=self.addressID)
