__ver__="$Id$"
from LinkInjector import *
from LinkSetInjector import *
from Clerk import *

def MockClerk(dbmap={}):
    from storage import MockStorage
    return Clerk(MockStorage(),dbmap)


