"""
Address / contact info

$Id$
"""
import zdc
import zikeshop

class Address(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_address")


