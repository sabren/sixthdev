
from strongbox import BlackBox, Private

class WhiteBox(BlackBox):
    """
    Base class for observable, injectable data
    objects with runtime type checking.
    """
    def __private__(self):
        self.private = Private()
        self.private.isDirty = True # so new objects get saved
        self.private.observers = []
        self.private.injectors = []

    ## for notifying other classes of changes:
    def addObserver(self, callback):
        self.private.observers.append(callback)
    def removeObserver(self, callback):
        self.private.observers.remove(callback)
    def notifyObservers(self, slot, value):
        for callback in self.private.observers:
            callback(self, slot, value)

    def onSet(self, slot, value):
        self.notifyObservers(slot, value)
        self.private.isDirty = True

    ## for lazy loading, etc:
    def addInjector(self, callback):
        self.private.injectors.append(callback)
    def removeInjector(self, callback):
        self.private.injectors.remove(callback)
    def notifyInjectors(self, slot):
        for callback in self.private.injectors:
            callback(self, slot)

    def onGet(self, slot):
        self.notifyInjectors(slot)
        
