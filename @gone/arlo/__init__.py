
from LinkInjector import *
from LinkSetInjector import *
from Clerk import *

def MockClerk():
    from storage import MockStorage
    return Clerk(MockStorage())


