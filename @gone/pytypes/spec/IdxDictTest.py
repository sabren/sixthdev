"""
test cases for IdxDict
"""
__ver__="$Id$"

import unittest
from pytypes import IdxDict

class IdxDictTest(unittest.TestCase):

    def check_IdxDict(self):
        idx = IdxDict()
        idx["a"] = 1
        idx["b"] = 2
        idx["c"] = 2
        idx["a"] = 0
        idx[1] = 1
        assert idx.keys() == ['a', 'b', 'c'], \
               "keys are wrong: %s" % str(idx.keys())
        assert idx[0] == 0, "index is wrong"
        assert idx[0:2] == [0, 1], \
               "slicing is wrong: %s" % str(idx[0:2])


    def check_nKeys(self):
        "check numeric keys"
        idx = IdxDict()
        idx[0] = "a"
        idx[1] = "b"
        assert idx.keys() == [0, 1], \
               "numeric keys are wrong: %s" % idk.keys()
        


    def check_lshift(self):
        idx = IdxDict()
        idx << "x"
        idx << "y"
        idx << "z"
        assert idx.keys() == [0, 1, 2], \
               "keys are wrong: %s" % str(idx.keys())
        assert idx.values() == ["x", "y", "z"], \
               "values are wrong: %s" % str(idx.values())


    def check_looping(self):
        idx = IdxDict()
        for item in idx:
            assert 0, "there shouldn't be anything in idx"

        idx << 1
        for item in idx:
            assert item==1, "wrong item"

        idx.clear()
        for item in idx:
            assert 0, "there shouldn't be anything in idx after .clear()"


    def check_negative(self):
        idx = IdxDict()
        idx << "abc"
        idx << "xyz"
        assert idx[-1] == "xyz", "-1 broke"
        assert idx[-2] == "abc", "-2 broke"
        try:
            bad = idx[-3]
            gotError = 0
        except IndexError:
            gotError = 1
        assert gotError, "-3 worked but should not have!"
        

    def check_repr(self):
        """
        really, this just exposes a bug if the keys are numbers...
        """
        idx = IdxDict()
        idx << "zero"
        assert repr(idx) == "{0: 'zero'}", \
               "wrong representation: %s" % repr(idx)
