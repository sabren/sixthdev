"""
zikeshop.State - states, with sales tax info
"""
__ver__="$Id$"
import zdc
import zikeshop

class State(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "ref_state")


    def get_salestax(self):
        import zikeshop
        return zikeshop.FixedPoint(self._data["salestax"])
