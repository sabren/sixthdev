"""
zikeshop.State - states, with sales tax info
"""
__ver__="$Id$"
import zdc
import zikeshop

class State(zdc.RecordObject):
    _tablename = "ref_state"

    def get_salestax(self):
        import zdc
        return zdc.FixedPoint(self._data["salestax"])
