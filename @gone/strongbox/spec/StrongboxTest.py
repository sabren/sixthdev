#@+leo

#@+node:0::@file StrongboxTest.py
#@+body
#@+at
# 
# Subject from the GoF Observer pattern.

#@-at
#@@code
__ver__="$Id$"

import unittest
import types
from strongbox import Strongbox, attr

class StrongboxTest(unittest.TestCase):

    def setUp(self):
        pass
        

    #@+others
    #@+node:1::Observers manage themselves with attach() and detatch()
    #@+body
    
    
    def check_attach(self):
        subject = Strongbox()
        observer = object()
        subject.attach(observer, onset="on_set")
        assert observer in [row[0] for row in subject.private.observers]
    
    
    def check_detach(self):
        subject = Strongbox()
        observer = object()
        subject.attach(object, onset="on_set")
        subject.detach(object)
        assert len(subject.private.observers) == 0
    #@-body
    #@-node:1::Observers manage themselves with attach() and detatch()
    #@+node:2::setattr and getattr trigger messages to the observers
    #@+body
    #@+at
    # 
    # First the setter. Setters are easy. This is very useful for
    # transparent persistence (a la ZODB) and also for general
    # Model/View/Controller and Observer pattern stuff.
    # 
    # As such, the events are fired AFTER the value is set
    # in the object. (Contrast to getter events, below...)

    #@-at
    #@@code
    
    def check_set_event(self):
        class Observer:
            def __init__(self):
                self.updated = 0
            def update(self, subject, name, value):
                self.updated = 1
                self.name = name
                self.value = value
        class Subject(Strongbox):
            name = attr(str)
        obs = Observer()
        sub = Subject()
        sub.attach(obs, onset="update")
        sub.name = "fred"
        assert obs.updated, "observer should have been updated on setattr"
        assert obs.name == "name"
        assert obs.value == "fred"
    

    #@+at
    # 
    # Getters, on the other hand are useful for lazy loading.
    # As such, the events get fired BEFORE the value is returned.
    # 
    # Of course, you couldn't call anything after you returned
    # a value anyway :)

    #@-at
    #@@code
    
    def check_get_event(self):
        class Observer:
            def __init__(self):
                self.called = 0
            def getter_called(self, subject, name):
                self.called += 1
                self.name = name
                subject.name = "wilma"
        class Subject(Strongbox):
            name = attr(str)
        obs = Observer()
        sub = Subject(name="wanda")
        sub.attach(obs, onget="getter_called")
        value = sub.name
        assert obs.called==1, "should have been called 1 time (vs %i)" % obs.called
        assert obs.name == "name"
        assert value == "wilma"

    #@-body
    #@-node:2::setattr and getattr trigger messages to the observers
    #@-others

       
    def tearDown(self):
        pass
#@-body
#@-node:0::@file StrongboxTest.py
#@-leo
