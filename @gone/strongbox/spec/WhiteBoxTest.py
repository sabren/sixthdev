# Subject from the GoF Observer pattern.

__ver__="$Id$"

import unittest
import types
from strongbox import WhiteBox, attr

class WhiteBoxTest(unittest.TestCase):

    # we implement the famous Gang of Four Observer pattern:
    
    def check_Observable(self):
        subject = WhiteBox()
        observer = object()
        subject.addObserver(observer)
        assert observer in subject.private.observers
        subject.removeObserver(observer)
        assert observer not in subject.private.observers

    # Injectable is like Observable, but instead of notifying
    # on set, we notify on get. That's so we can lazy load objects:

    def check_Injectable(self):
        subject = WhiteBox()
        injector = object()
        subject.addInjector(injector)
        assert injector in subject.private.injectors
        subject.removeInjector(injector)
        assert injector not in subject.private.injectors
   

    # First the setter. Setters are easy. This is very useful for
    # transparent persistence (a la ZODB) and also for general
    # Model/View/Controller and Observer pattern stuff.
    # 
    # As such, the events are fired AFTER the value is set
    # in the object. (Contrast to getter events, below...)

    def check_set_event(self):
        class Observer:
            def __init__(self):
                self.updated = False
            def update(self, subject, name, value):
                self.updated = True
                self.name = name
                self.value = value
        class Subject(WhiteBox):
            name = attr(str)

        # first, try with no observers:
        sub = Subject()
        sub.name='wilbur'
        assert sub.name=='wilbur', sub.name

        # now add an observer:
        obs = Observer()
        assert not obs.updated
        sub.addObserver(obs.update)
        sub.name = "fred"
        assert obs.updated, "observer should have been updated on setattr"
        assert obs.name == "name"
        assert obs.value == "fred"
    

    # Getters, on the other hand are useful for lazy loading.
    # As such, the events get fired BEFORE the value is returned.
    # 
    # Of course, you couldn't call anything after you returned
    # a value anyway :)

    def check_get_event(self):
        class Injector:
            def __init__(self):
                self.called = 0
            def getter_called(self, subject, name):
                self.called += 1
                self.name = name
                subject.name = "wilma"
        class Subject(WhiteBox):
            name = attr(str)
        inj = Injector()
        sub = Subject(name="wanda")
        sub.addInjector(inj.getter_called)
        value = sub.name
        assert inj.called==1, \
               "should have been called 1 time (vs %i)" % inj.called
        assert inj.name == "name"
        assert value == "wilma", value

    def test_isDirty(self):
        """
        this is for arlo...
        """
        class Dirt(WhiteBox):
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
