"""
Type labels..
"""
__ver__="$Id$"

import zdc

class Type(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "plan_type")

    ## RecordObject constructors ###########################
    
    def _new(self):
        self.__super._new(self)
        self._data['label'] = ""
