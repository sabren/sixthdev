"""
Contact - name, phone, and address..
"""
__ver__="$Id$"


from strongbox import Strongbox, attr

class Contact(Strongbox):
    ID = attr(int)
    userID = attr(int, default=0)
    fname = attr(str)
    lname = attr(str)
    email = attr(str)
    address1 = attr(str)
    address2 = attr(str)
    address3 = attr(str)
    city = attr(str)
    stateCD = attr(str)
    postal = attr(str)
    countryCD = attr(str)
    phone = attr(str)
    
    
    def set_email(self, value):
        #@TODO: test set_email!
        if value:
            import zdc.isvalid
            if not zdc.isvalid.email(value):
                raise ValueError, "'%s' is not a valid email address" % value
        self._data["email"]=value
