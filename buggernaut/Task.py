"""
Task: stuff to do.
"""
__ver__="$Id$"

import zdc

class Task(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "plan_task")
    _links = {
## eg:
##        "details": [zdc.LinkSet, zikeshop.Detail, "saleID"],
        }

    ## RecordObject constructors ###########################
    
    def _init(self):
        #@TODO: override this for things that should ALWAYS happen.
        pass

    def _new(self):
        self.__super._new(self)
        self._data['author_userID'] = 0
        self._data['owner_userID'] = 0
        self._data['summary'] = ''
        self._data['detail'] = ''
        self._data['typeID'] = 0
        self._data['statusID'] = 0
        self._data['targetDate'] = None
        self._data['createDate'] = zdc.TIMESTAMP
        self._data['risk'] = 5
        self._data['reward'] = 5
        self._data['hrsOrig'] = None
        self._data['hrsCurr'] = None
        self._data['hrsElap'] = None

    def _fetch(self, **where):
        apply(self.__super._fetch, (self,), where)
        #@TODO: fetch any extra data here.. [linksets, etc..] {notes}

    ## other RecordObject methods ###########################
        
