#
# testIdxDict.py - test cases for zdc.IdxDict

import unittest
import zdc.IdxDict


class IdxDictTestCase(unittest.TestCase):

    def check_IdxDict(self):
        import IdxDict
        idx = IdxDict.IdxDict()
        idx["a"] = 1
        idx["b"] = 2
        idx["c"] = 2
        idx["a"] = 0
        idx[1] = 1
        assert idx.keys() == ['a', 'b', 'c'], "keys are wrong"
        assert idx[0] == 0, "index is wrong"

