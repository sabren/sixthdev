
from Index import *
from WordHash import *

NEXTNUM = "\t:nextnum"


def intListToStr(self, intList):
    import array
    return array.array("I", intList).tostring()

def strToIntList(self, str):
    import array
    return array.array("I", str).tolist()

