
import unittest
import types
from strongbox import MetaBox, Private, attr

class MetaBoxTest(unittest.TestCase):
    def test_simple(self):

        Person = MetaBox("Person", (), {
            "name" : attr(str, okay=['fred','wanda'], default="fred"),
        })

        assert type(Person) == MetaBox
        assert isinstance(Person.name, attr)
        assert Person.name.okay == ['fred','wanda']
        assert Person.name.__name__ == "name"
        assert Person.name.__owner__ == Person

        # That's really about all we can test here.
        #
        # The metaclass produces a class, but the
        # class isn't very useful at that point.
        # It's expecting to have methods like
        # onSet, and onGet, and a .private ...
        # but those things don't exist at this
        # point in the object's lifecycle.
        #
        # That's why you subclass BlackBox
        # or StrongBox instead of using MetaBox
        # directly.

if __name__=="__main__":
    unittest.main()
    
