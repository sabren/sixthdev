"""
testObject - test cases for zdc.Object
"""
__ver__="$Id$"

import unittest
import zdc.Object


class TestObj(zdc.Object):
    def _new(self):
        pass
    def _init(self):
        pass


class ObjectTestCase(unittest.TestCase):

    def check_lockDefault(self):
        tobj = TestObj()
        assert tobj._isLocked == 0, \
               "oh no! zdc.Object isn't unlocked by default!"


    def check_getMethod(self):
        class GetClass(TestObj):
            aaa = 5
            def get_aaa(self):
                return 1
            def get_xxx(self):
                return 1

        obj = GetClass()
        assert obj.xxx == 1, \
               "get_XXXX() methods don't work!"

        ## I really wish this worked, but if it
        ## ever does, I'll have to ZDC!
        obj = GetClass()
        assert obj.aaa == 5, \
               "wahoo! get_XXXX() methods are finally called before __dict__!"


    def check_setMethod(self):
        class SetClass(TestObj):
            def set_xxx(self, value):
                self.xyz = value

        obj = SetClass()
        obj.xxx = "testme!"
        assert obj.xyz == "testme!", \
               "set_XXX() methods don't work!"

