"""
Notes about a particular task.
"""
__ver__="$Id$"

import zdc
import zikebase
zikebase.load("Content")

class Note(zikebase.Content):
    __super = zikebase.Content
    _table = zdc.Table(zikeshop.dbc, "plan_task_note")

    ## RecordObject constructors ###########################

    def _new(self):
        self.__super._new(self)
        self._data['taskID'] = 0