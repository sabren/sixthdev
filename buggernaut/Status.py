"""
Status labels..
"""
__ver__="$Id$"

import zdc

class Status(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "plan_status")

    ## RecordObject constructors ###########################
    
    def _new(self):
        self.__super._new(self)
        self._data['label'] = ""
