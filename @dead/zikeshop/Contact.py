"""
Contact - name, phone, and address..
"""
__ver__="$Id$"


import zdc

class Contact(zdc.RecordObject):
    __super = zdc.RecordObject
    _tablename = "base_contact"

    def _new(self):
        self.__super._new(self)
        self._data["userID"]=0
        self._data["fname"]=""
        self._data["lname"]=""
        self._data["email"]=""
        self._data["address1"]=""
        self._data["address2"]=""
        self._data["address3"]=""
        self._data["city"]=""
        self._data["stateCD"]=""
        self._data["postal"]=""
        self._data["countryCD"]="US"
        self._data["phone"]=""
    
    def set_email(self, value):
        #@TODO: test set_email!
        if value:
            import zdc.isvalid
            if not zdc.isvalid.email(value):
                raise ValueError, "'%s' is not a valid email address" % value
        self._data["email"]=value
