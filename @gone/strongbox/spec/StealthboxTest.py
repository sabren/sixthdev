#@+leo

#@+node:0::@file StealthboxTest.py
#@+body
"""
test cases for Strongbox
"""
__ver__="$Id$"

import unittest
import types
from strongbox import Strongbox, attr

class StealthboxTest(unittest.TestCase):

    def setUp(self):
        pass
        

    #@+others
    #@+node:1::Strongbox uses metaclasses to provide its magic
    #@+body
    #@+at
    # 
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

    #@-at
    #@@code
    
    def check_looks_like_a_class(self):
        class X(Strongbox):
            pass
        assert isinstance(X(), Strongbox)
    #@-body
    #@-node:1::Strongbox uses metaclasses to provide its magic
    #@+node:2::Strongbox attributes are defined as class variables
    #@+body
    #@+at
    # 
    # Attributes must be present in the class definition.

    #@-at
    #@@code
    
    def check_slots(self):
        class Slotmachine(Strongbox):
            a = attr(int, default=1)
            b = attr(int, default=2)
            c = attr(int, default=3)
        xinst = Slotmachine() 
        xinst.a = 1 # should work
        try:
           err = 0
           xinst.d = 4
        except AttributeError:
           err = 1
        assert err, "assigning to nonexistent slot d should have failed."
    #@-body
    #@-node:2::Strongbox attributes are defined as class variables
    #@+node:3::Strongbox turns accessors into properties
    #@+body
    #@+at
    # 
    # Specifically, it should automatically create properties from
    # methods called get_XXX and set_XXX:

    #@-at
    #@@code
    
    def check_properties(self):
        class X(Strongbox):
            def get_a(self): return 1
            get_b = lambda self: 2
            c = attr(int)
            d = attr(int)
            def set_c(self, value): self.d = 4
        instance = X()
        assert instance.a == 1
        assert instance.b == 2
        instance.c = 3
        assert instance.c == 0 # see check_default_defaults
        assert instance.d == 4, instance.d
    #@-body
    #@-node:3::Strongbox turns accessors into properties
    #@+node:4::Private variables are explicitly private
    #@+body
    #@+at
    # 
    # All strongbox instances have a "private" namespace, which
    # lets them store private variables explicitly. (This is necessary
    # because self.xxx = yyy would cause an AttributeError if xxx is
    # not defined up front as an attrbute)

    #@-at
    #@@code 
    def check_private(self):
        s = Strongbox()
        assert hasattr(s, "private")
        s.private.c = 1
        assert s.private.c == 1
    #@-body
    #@-node:4::Private variables are explicitly private
    #@+node:5::Attributes have defaults, but can be initialized via the constructor
    #@+body
    
    
    def check_defaults(self):
        class Foo(Strongbox):
            bar = attr(int, default=5)  
        foo = Foo()
        assert foo.bar ==5
    
    def check_constructor(self):
        class Foo(Strongbox):
            bar = attr(int, default=5)  
        foo = Foo(bar=12)
        assert foo.bar == 12
    #@-body
    #@-node:5::Attributes have defaults, but can be initialized via the constructor
    #@+node:6::Without explicit defaults, strings default to '', ints and longs to 0
    #@+body
    
    def check_default_defaults(self):
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
    #@-body
    #@-node:6::Without explicit defaults, strings default to '', ints and longs to 0
    #@+node:7::Other types pass defaults to the constructor
    #@+body
    
    def check_othertypes(self):
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
    #@-body
    #@-node:7::Other types pass defaults to the constructor
    #@+node:8::Attributes use static typing
    #@+body
    
    def check_static_typing(self):
        class Foo(Strongbox):
           bar = attr(int)
        foo = Foo()
        try:
           goterr = 0
           foo.bar = "not an int value"
        except TypeError:
           goterr = 1
        assert goterr, "should get TypeError assigning string to int attr"
    
    
    def check_okay_lambda(self):
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
    
    
    def check_okay_list(self):
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
    
        
    def check_okay_regexp(self):
        class UsCitizen(Strongbox):
            ssn = attr(str, r"\d{3}-?\d{2}-?\d{4}")
        
        elmer = UsCitizen()
        elmer.ssn = "404-44-4040" # should work
        try:
            goterr = 0
            elmer.ssn = "867-5309"
        except ValueError:
            goterr = 1
        assert goterr, "ssn regexp should reject even the most famous phone number in america..."
    #@-body
    #@-node:8::Attributes use static typing
    #@+node:9::Attributes allow "None" by default
    #@+body
    #@+at
    # 
    # But of course, we can turn it off...
    # 

    #@-at
    #@@code
    
    def check_allowNone(self):
        class Foo(Strongbox):
           bar = attr(int)
        foo = Foo()
        try:
           goterr = 0
           foo.bar = None
        except ValueError:
           goterr = 1
        assert not goterr, "assigning None didn't work!"
    
    
    def check_dontAllowNone(self):
        class Foo(Strongbox):
           bar = attr(int,allowNone=0)
        foo = Foo(bar=15)
        try:
           goterr = 0
           foo.bar = None
        except ValueError:
           goterr = 1
        assert goterr, "assigning None should have failed!"
    #@-body
    #@-node:9::Attributes allow "None" by default
    #@-others

       
    def tearDown(self):
        pass
#@-body
#@-node:0::@file StealthboxTest.py
#@-leo
