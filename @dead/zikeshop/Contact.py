"""
Contact - name, phone, and address..
"""
__ver__="$Id$"

from strongbox import Strongbox, attr
from pytypes import EmailAddress

class Contact(Strongbox):
    ID = attr(int)
    userID = attr(int, default=0)
    fname = attr(str)
    lname = attr(str)
    email = attr(EmailAddress)
    address1 = attr(str)
    address2 = attr(str)
    address3 = attr(str)
    city = attr(str)
    stateCD = attr(str)
    postal = attr(str)
    countryCD = attr(str)
    phone = attr(str)
    
