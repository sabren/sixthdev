import unittest
import new

"""
this just lets you write test cases inline,
making it a little easier to write 'narrative'
documents that mix commentary and tests.
"""

def testcase(f):
    # create a new class:
    class NewTest(unittest.TestCase):
        pass

    # add the test() method
    setattr(NewTest, "test",
            new.instancemethod(f, None, NewTest))

    # and return it
    return NewTest

