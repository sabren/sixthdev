"""
zikeshop.State - states, with sales tax info
"""
__ver__="$Id$"
import zdc
import zikeshop

class State(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "shop_state", rowid="CD")


    def get_salestax(self):
        import zdc
        return zdc.FixedPoint(self._data["salestax"])
