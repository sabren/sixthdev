

import zdc
import zikeshop

class Card(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_card")
    _defaults = {}
    _tuples = []

