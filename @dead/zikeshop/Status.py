
import zdc
import zikeshop

class Status(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_status")
