
__ver__="$Id$"

import strongbox

class LinkInjector:
    def __init__(self, clerk, fclass, fID):
        """
        Registers a callback so that when getattr(box, atr)
        is called, the object of box.atr's type with given ID
        is loaded from sto and injected into box.

        In other words, this provides lazy loading for
        strongboxen.
        """
        self.clerk = clerk
        self.fID = fID
        self.fclass = fclass

    def inject(self, stub, name):
        """
        This injects data into the stub.

        WARNING: It replaces the entire .private
        object with a fresh instance, which means any
        state information will disappear. That is why
        it's imperative that you call .notifyInjectors()
        before manipulating .private in your Strongbox.

        However, it does preserve observers and
        any other injectors attached to the stub.
        """
        if name == "ID":
            pass # stubs have ID, so no need to load
        else:
            old = stub.private

            # we call fetch so we get stubs for all the
            # new object's dependents
            new = self.clerk.fetch(self.fclass, self.fID).private

            # inject the data:
            for slot in self.fclass.__attrs__:
                setattr(old, slot, getattr(new, slot))
            old.isDirty = False

            # since we might have observers, we'll
            # let them know:
            stub.notifyObservers("inject", "inject")
            stub.removeInjector(self.inject)
