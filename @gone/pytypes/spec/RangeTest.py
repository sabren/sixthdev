"""
RangeTest
"""
__ver__="$Id$"

import unittest
from pytypes import InclusiveRange, ExclusiveRange, PythonicRange

class RangeTest(unittest.TestCase):

    def test_inclusive(self):
        irange = InclusiveRange(1, 3)
        assert 1 in irange
        assert 2 in irange
        assert 3 in irange

    def test_exclusive(self):
        erange = ExclusiveRange(1, 3)
        assert 1 not in erange
        assert 2 in erange
        assert 3 not in erange

    def test_pythonic(self):
        prange = PythonicRange(1, 3)
        assert 1 in prange
        assert 2 in prange
        assert 3 not in prange
    

if __name__=="__main__":
    unittest.main()

