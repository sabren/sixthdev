"""
Task: stuff to do.
"""
__ver__="$Id$"

import zdc, zikebase

class Task(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikebase.dbc, "plan_task")
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
        self._data['owner'] = "michal"
        self._data['status'] = "open"
        self._data['priority'] = "medium"
        self._data['project'] = "zikeshop"
        self._data['risk'] = "medium"
        self._data['targetDate'] = None
        self._data['createDate'] = zdc.TIMESTAMP
        self._data['hrsOrig'] = None
        self._data['hrsCurr'] = None
        self._data['hrsElap'] = None

    def _fetch(self, **where):
        apply(self.__super._fetch, (self,), where)
        #@TODO: fetch any extra data here.. [linksets, etc..] {notes}

    ## other RecordObject methods ###########################

    def get_hrsElap(self):
        if self._data["hrsElap"]:
            return zdc.FixedPoint(self._data["hrsElap"])

    def get_hrsOrig(self):
        if self._data["hrsOrig"]:
            return zdc.FixedPoint(self._data["hrsOrig"])

    def get_hrsCurr(self):
        if self._data["hrsCurr"]:
            return zdc.FixedPoint(self._data["hrsCurr"])

    def set_hrsCurr(self, value):
        if self._data["hrsOrig"] is None:
            self.hrsOrig = value
        self._data["hrsCurr"]=value

    def get_hrsLeft(self):
        return (self.hrsCurr or 0) - (self.hrsElap or 0)
    
    def getEditableAttrs(self):
        return self.__super.getEditableAttrs(self) + ['hrsLeft']


    def set_targetDate(self, value):
        import date
        self._data["targetDate"]=date.us2sql(value)

## this should work, but there's a line in RecordObject.save()
## that calls getattr instead of reading from ._data directly.
## unforunately, a lot of code is depending on that bug, so I
## put off making the change for now.  (0310.2001)
##
##     def get_targetDate(self):
##         import date
##         return date.sql2us(self._data["targetDate"])


    ##### options for select boxes ################

    def opt_status(self):
        return ("open", "closed", "ignore")

    def opt_priority(self):
        return ("low", "medium", "high", "critical")

    def opt_risk(self):
        return ("low", "medium", "high", "unknown")

    def opt_owner(self):
        return ("michal", "zach", "nobody")

    def opt_project(self):
        projs=["zikeshop", "zikebase", "zikeplan",
               "blogdrive", "buggernaut", "linkwatcher",
               "ransacker", "zikeshop/express", "zikeshop/ultra",
               "weblib", "zebra", "zdc", "sixthday"]
        projs.sort()
        return tuple(projs)
               

