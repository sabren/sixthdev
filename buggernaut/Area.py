__ver__="$Id$"

from strongbox import *
auto =None

class Area(Strongbox):
    ID = attr(int, default=auto)
    area = attr(str)
    
