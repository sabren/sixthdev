#
# testIdxDict.py - test cases for zdc.IdxDict

import unittest
import zdc.Object


class TestObj(zdc.Object):
    def __init__(self):
        pass


class ObjectTestCase(unittest.TestCase):

    def check_lockDefault(self):
        tobj = TestObj()
        assert tobj._isLocked == 0, "oh no! zdc.Object isn't unlocked by default!"


    def check_getMethod(self):
        class GetClass(TestObj):
            def get_xxx(self):
                return 1

        obj = GetClass()
        assert obj.xxx == 1, "get_XXXX() methods don't work!"



    def check_setMethod(self):
        class SetClass(TestObj):
            def set_xxx(self, value):
                self.xyz = value

        obj = SetClass()
        obj.xxx = "testme!"
        assert obj.xyz == "testme!", "set_XXX() methods don't work!"

