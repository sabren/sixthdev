"""
An Event Detail.
"""
__ver__="$Id$"

import zdc
import zikeshop

class Detail(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_detail")
    _defaults = {
        "eventID": 0,
        "from_locationID" : 0,
        "to_locationID" : 0,
        "quantity" : 0,        
        }


    def get_product(self):
        return zikeshop.Product(ID=self.productID)
