"""
Notes about a particular task.
"""
__ver__="$Id$"

from strongbox import *
from pytypes import *

class Note(Strongbox):
    userID  = attr(int, default=0)    
    taskID  = attr(int, default=0)
    content = attr(str)    
    tsCreate = attr(DateTime, default="now")
    tsUpdate = attr(DateTime, default="now")
    
