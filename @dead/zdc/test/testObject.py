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

    def check_lock(self):
        """
        Objects should be locked as soon as they're initialized.
        If you want to do stuff to locked fields, do it in
        _init(), _fetch(), or _new().
        """
        tobj = TestObj()
        assert tobj._isLocked, \
               "oh no! zdc.Object instances aren't locked!"

    def check_locks(self):
        "Locked attributes should be readonly"
        class TestObj2(TestObj):
            _locks = ["ABC"]
            def _new(self):
                self.ABC = 5

        tobj = TestObj2()
        try:
            gotError = 0
            tobj.ABC = 6
        except AttributeError:
            gotError = 1

        assert gotError, \
               "Didn't get an AttributeError assigning to locked field."

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
                self._data['xyz'] = value

        obj = SetClass()
        obj.xxx = "testme!"
        assert obj.xyz == "testme!", \
               "set_XXX() methods don't work!"

