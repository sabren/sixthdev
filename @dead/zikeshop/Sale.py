

import zdc
import zikeshop

class Sale(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_sale")
    _defaults = {}
    _tuples = []

