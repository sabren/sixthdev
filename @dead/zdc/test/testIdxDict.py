#
# testIdxDict.py - test cases for zdc.IdxDict

import unittest
import zdc


class IdxDictTestCase(unittest.TestCase):

    def check_IdxDict(self):
        idx = zdc.IdxDict()
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
        idx = zdc.IdxDict()
        idx[0] = "a"
        idx[1] = "b"
        assert idx.keys() == [0, 1], \
               "numeric keys are wrong: %s" % idk.keys()
        


    def check_lshift(self):
        idx = zdc.IdxDict()
        idx << "x"
        idx << "y"
        idx << "z"
        assert idx.keys() == [0, 1, 2], \
               "keys are wrong: %s" % str(idx.keys())
        assert idx.values() == ["x", "y", "z"], \
               "values are wrong: %s" % str(idx.values())
