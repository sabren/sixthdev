
from arlo import Clerk

class CallbackClerk(Clerk):
    """
    This class allows you to set up callbacks
    to trigger events whenever an object of a
    particular class gets stored.
    """

    def __init__(self, *args, **kwargs):
        super(CallbackClerk, self).__init__(*args, **kwargs)
        self._callbacks = {}       
    
    def onStore(self, klass, dowhat):
        self._callbacks.setdefault(klass,[])
        self._callbacks[klass].append(dowhat)
        
    def store(self, thing):
        thing = super(CallbackClerk, self).store(thing)
        klass = thing.__class__
        for callback in self._callbacks.get(klass, []):
            callback(thing)
        return thing
