
from LinkInjector import *
from Clerk import *

def MockClerk():
    from storage import MockStorage
    return Clerk(MockStorage())


