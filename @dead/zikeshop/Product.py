
import zdc
import zikeshop

class Product(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_product")
    _defaults = {}

    
