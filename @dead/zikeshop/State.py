"""
zikeshop.State - states, with sales tax info
"""
__ver__="$Id$"
import zdc
import zikeshop
from pytypes import FixedPoint

class State(zdc.RecordObject):
    _tablename = "ref_state"

    def get_salestax(self):
        return FixedPoint(self._data["salestax"])
