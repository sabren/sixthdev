#
# testIdxDict.py - test cases for zdc.IdxDict

import unittest
import zdc.Object


class ObjectTestCase(unittest.TestCase):

    def check_lockDefault(self):

        ## first, create a dummy class
        class LockObj(zdc.Object):
            def __init__(self):
                pass

        lobj = LockObj()
        assert lobj._isLocked == 0, "oh no! zdc.Object isn't unlocked by default!"

