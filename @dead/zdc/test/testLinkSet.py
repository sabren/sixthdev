"""
unit tests for linkSet
"""
__ver__="$Id$"
import unittest
import zdc

class LinkSetTestCase(unittest.TestCase):

    def setUp(self):
        # a link between two objects:
        self.obj = zdc.Object()
        self.lset = zdc.LinkSet(self.obj, zdc.Object)

    def check_constructor(self):
        """
        Ensure the linkset it properly created.
        """
        assert len(self.lset) == 0, \
               "wrong default length"
        assert self.lset.owner is self.obj, \
               "wrong owner"
        assert self.lset.rClass is zdc.Object, \
               "wrong rClass"

    def check_lshift(self):
        """
        Ensure that objects of wrong type cannot belong to the set,
        and that objects of correct type can belong to the set.
        """
        class FakeClass:
            pass

        ## make sure the wrong thing doesn't work..
        try:
            gotError=0
            self.lset << FakeClass()
        except TypeError:
            gotError=1

        assert gotError, \
               "Doesn't catch invalid type..."

        ## make sure the right thing does work
        try:
            obj = zdc.Object()
            gotError=0
            self.lset << obj
        except:
            gotError=1
        assert not gotError, \
               "Got error on proper type."
        assert len(self.lset) == 1, \
               "didn't add right number of objects."
        assert self.lset[0] == obj, \
               "didn't assign correct object."
            
