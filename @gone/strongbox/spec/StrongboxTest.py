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
from Strongbox import Strongbox

class StrongboxTest(unittest.TestCase):

    def setUp(self):
        pass
        

    #@+others
    #@+node:1::Observers manage themselves with attach() and detatch()
    #@+body
    
    
    def check_attach(self):
        subject = Strongbox()
        observer = object()
        subject.attach(observer)
        assert observer in subject.private.observers
    
    
    def check_detach(self):
        subject = Strongbox()
        observer = object()
        subject.attach(object)
        subject.detach(object)
        assert len(subject.private.observers) == 0
    #@-body
    #@-node:1::Observers manage themselves with attach() and detatch()
    #@+node:2::subject.notify() sends messages to all the observers
    #@+body
    
    def check_notify(self):
        class Observer:
            def update(self, subject): self.updated = 1
        obs = Observer()
        sub = Strongbox()
        sub.attach(obs)
        sub.notify()
        assert obs.updated, "observer should have been updated"
    #@-body
    #@-node:2::subject.notify() sends messages to all the observers
    #@+node:3::setattr fires off notify
    #@+body
    
    def check_setevent(self):
    	pass

    #@-body
    #@-node:3::setattr fires off notify
    #@-others

       
    def tearDown(self):
        pass
#@-body
#@-node:0::@file StrongboxTest.py
#@-leo
