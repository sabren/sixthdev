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
        self.fname=""
        self.lname=""
        self.email=""
        self.address1=""
        self.address2=""
        self.address3=""
        self.city =""
        self.stateCD=""
        self.postal=""
        self.country="US"
        self.phone=""
    
    def set_email(self, value):
        #@TODO: test set_email!
        if value:
            import zdc.isvalid
            if not zdc.isvalid.email(value):
                raise ValueError, "'%s' is not a valid email address" % value
        self._data["email"]=value
