"""
Contact - name, phone, and address..
"""
__ver__="$Id$"

import zikebase
import zdc

class Contact(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikebase.dbc, "base_contact")

    def _new(self):
        self.__super._new(self)
        self.userID=0
    
    def set_email(self, value):
        #@TODO: test set_email!
        if value:
            import zdc.isvalid
            if not zdc.isvalid.email(value):
                raise ValueError, "value is not a valid email address"
        self._data["email"]=value
