"""
Address / contact info

$Id$
"""
import zdc
import zikeshop


#@TODO: get rid of this!
class Address(zdc.RecordObject):
    _table = zdc.Table(zikeshop.dbc, "base_contact")

    def get_customerID(self):
        return self.userID

    def set_customerID(self, value):
        self.userID = value


