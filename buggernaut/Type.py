"""
Type labels..
"""
__ver__="$Id$"

import zdc, zikebase

class Type(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikebase.dbc, "plan_type")

    ## RecordObject constructors ###########################
    
    def _new(self):
        self.__super._new(self)
        self._data['label'] = ""
