"""
Contact - name, phone, and address..
"""
__ver__="$Id$"

import zikebase
import zdc

class Contact(zdc.RecordObject):
    _table = zdc.Table(zikebase.dbc, "base_contact")
    _defaults = {"userID": 0}   

    
