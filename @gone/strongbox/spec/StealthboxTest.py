"""
test cases for Strongbox
"""
__ver__="$Id$"

import unittest
import types
from strongbox import Strongbox, attr, link, linkset, StrongboxError
from pytypes import Date

class StealthboxTest(unittest.TestCase):

    def setUp(self):
        pass

    ## Strongbox uses metaclasses to provide its magic

    # Strongbox is a Metaclass
    # 
    # What's a metaclass? It's a class representing a class.
    # 
    # http://www.python.org/2.2/descrintro.html#metaclasses
    # 
    # For example, in python 2.2, there are old-style
    # classes and new-style classes. They don't work
    # exactly the same, but they're both types of classes.
    # 
    # Strongboxes are another type of class, which makes
    # Strongbox a metaclass. Make sense?
    # 
    # But it should look just like a normal class:

    def test_looks_like_a_class(self):
        class X(Strongbox):
            pass
        assert isinstance(X(), Strongbox)

    ## Strongbox attributes are defined as class variables

    # Attributes must be present in the class definition.

    def test_slots(self):
        class Slotmachine(Strongbox):
            a = attr(int, default=1)
            b = attr(int, default=2)
            c = attr(int, default=3)
        xinst = Slotmachine() 
        xinst.a = 1 # should work
        try:
           err = 0
           xinst.d = 4
        except StrongboxError:
           err = 1
        assert err, "assigning to nonexistent slot d should have failed."

    ## All attributes show up in __attrs__
    # @TODO: it might make sense for links and linksets to go in __links__
    # since they're slightly different. This would most likely involve
    # refactoring the way link subclasses attr, because they do share
    # some features. (link can be assigned to, linkset cannot)
    # I need to work this out.

    def test_magicmeta(self):
        class X(Strongbox): pass
        class Y(Strongbox):
            a = attr(int)
            b = attr(str)
            c = link(X)
            d = link(X)
        assert "a" in Y.__attrs__
        assert "b" in Y.__attrs__
        assert "c" in Y.__attrs__
        assert "d" in Y.__attrs__
            

    ## Strongbox turns accessors into properties

    # Specifically, it should automatically create properties from
    # methods called get_XXX and set_XXX:

    def test_properties(self):
        class X(Strongbox):
            def get_a(self): return 1
            get_b = lambda self: 2
            c = attr(int)
            d = attr(int)
            e = attr(int, default=5)
            def set_c(self, value): self.d = 4
            def set_e(self, value): pass
        instance = X()
        assert instance.a == 1
        assert instance.b == 2
        instance.c = 3
        assert instance.c == 0 # see test_default_defaults
        assert instance.d == 4, instance.d

        # e is a special case, because a default in duckbill.Account
        # wasn't working when there was also an accessor.
        # (but I think this issue is with Cyclic, not strongbox)
        assert instance.e == 5

    def test_nestedError(self):
        class NestedError(Strongbox):
            def get_a(self):
                return self.b
        ne = NestedError()
        try:
            a = ne.a
        except StrongboxError, e:
            assert str(e) == "'b' is not a valid attribute for NestedError", \
                   "got wrong error: %s" % e
        else:
            self.fail("Should have gotten an StrongboxError!")


    ## Private variables are explicitly private

    # All strongbox instances have a "private" namespace, which
    # lets them store private variables explicitly. (This is necessary
    # because self.xxx = yyy would cause an StrongboxError if xxx is
    # not defined up front as an attrbute)

    def test_private(self):
        s = Strongbox()
        assert hasattr(s, "private")
        s.private.c = 1
        assert s.private.c == 1


    ## Attributes have defaults, but can be initialized via the constructor
    
    def test_defaults(self):
        class Foo(Strongbox):
            bar = attr(int, default=5)  
        foo = Foo()
        assert foo.bar ==5
    
    def test_constructor(self):
        class Foo(Strongbox):
            bar = attr(int, default=5)  
        foo = Foo(bar=12)
        assert foo.bar == 12


    ## Without explicit defaults, strings default to '', ints and longs to 0

    def test_default_defaults(self):
        class Foo(Strongbox):
            m_str = attr(str)
            m_int = attr(int)
            m_long = attr(float)
            m_float = attr(float)
            n_int = attr(int, default=None)
            n_str = attr(str, default=None)
        foo = Foo()
        assert foo.m_str == ''
        assert foo.m_int == 0
        assert foo.m_long == 0
        assert foo.m_float == 0
        assert foo.n_int is None
        assert foo.n_str is None

    ## Other types pass defaults to the constructor
    
    def test_othertypes(self):
        class UpCase:
            def __init__(self, value): self.value = str(value).upper()
            def __cmp__(self, other): return cmp(self.value, other)
            def __repr__(self): return value
        class Foo(Strongbox):
            bar = attr(UpCase, default="xyz")
            abc = attr(str, default="xyz")
        foo = Foo()
        assert foo.bar == "XYZ", foo.bar
        assert foo.abc == "xyz", foo.abc


    ## Attributes use static typing
    
    def test_static_typing(self):
        class Foo(Strongbox):
           bar = attr(int)
        foo = Foo()
        try:
           goterr = 0
           foo.bar = "not an int value"
        except TypeError:
           goterr = 1
        assert goterr, "should get TypeError assigning string to int attr"
    
    
    def test_okay_lambda(self):
        class Foo(Strongbox):
            bar = attr(int, lambda x: 5 < x < 10)
        foo = Foo()
        foo.bar = 7 # should work
        try:
           goterr = 0
           foo.bar = 10
        except ValueError:
            goterr = 1
        assert goterr, "the lambda should have rejected bar=10"
    
    
    def test_okay_list(self):
        class Paint(Strongbox):
            color = attr(str, ["red", "green", "blue"])
        p = Paint()
        p.color = "red" # should work
        try:
            goterr = 0
            p.color = "orange"
        except ValueError:
            goterr = 1
        assert goterr, "values not in the list should be rejected"
    
        
    def test_okay_regexp(self):
        class UsCitizen(Strongbox):
            ssn = attr(str, r"\d{3}-?\d{2}-?\d{4}")
        
        elmer = UsCitizen()
        elmer.ssn = "404-44-4040" # should work
        try:
            goterr = 0
            elmer.ssn = "867-5309"
        except ValueError:
            goterr = 1
        assert goterr, \
               "ssn regexp should reject phone numbers - even famous ones"


    ## dealing with None / empty strings ########################
    
    def test_allowNone(self):
        """
        Attributes allow "None" by default
        """
        class Foo(Strongbox):
           bar = attr(int)
        foo = Foo()
        try:
           goterr = 0
           foo.bar = None
        except ValueError:
           goterr = 1
        assert not goterr, "assigning None didn't work!"    
   
    def test_dontAllowNone(self):
        """
        We can disallow None if we want.
        """
        class Foo(Strongbox):
           bar = attr(int,allowNone=0)
        foo = Foo(bar=15)
        try:
           goterr = 0
           foo.bar = None
        except ValueError:
           goterr = 1
        assert goterr, "assigning None should have failed!"

    def test_emptyString(self):
        """
        Should convert empty strings to None, unless
        it actually IS a string. This is so we can
        pass None in from an HTML form.

        Really, I don't think the browser should send an
        empty string, but IE5.00.2614.3500 sure seems to,
        so let's deal with it. :)
        """
        class Foo(Strongbox):
            i = attr(int)
            s = attr(str)
            d = attr(Date)
        f = Foo()
        f.i = ""; assert f.i is None
        f.s = ""; assert f.s is ""
        f.d = ""; assert f.d is None

        
    def test_isDirty(self):
        """
        this is for arlo...
        """
        class Dirt(Strongbox):
            x = attr(str)
        d = Dirt()
        # we start out dirty so that we get saved
        # (even if we're blank!)
        assert d.private.isDirty
        d = Dirt(x="dog")
        assert d.private.isDirty

        # but if something marks us clean, and then
        # we change, we should be dirty again!
        d.private.isDirty = 0
        d.x = "cat"
        assert d.private.isDirty

    def test_inheritance(self):
        class Dad(Strongbox):
            nose = attr(str, default="big")
        class Son(Dad):
            pass
        assert Son().nose == "big"
       
    def tearDown(self):
        pass
    
if __name__=="__main__":
    unittest.main()
    
