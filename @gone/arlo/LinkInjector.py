
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
        if name != "ID":
            data = self.clerk.fetch(self.fclass, self.fID)
            ## can't just call stub.update() because it
            ## was trying to assign linksets, which raises
            ## an AttributeError
            #
            # @TODO: I'm not sure I believe that.
            # is this a good place for a memento pattern?
            #
            # ah.. we don't want fetch... we want to get
            # a memento from the database... no wonder.
            #
            for name, attr in stub.__attrs__.items():
                ## @TODO: this doesn't seem very object-oriented. :/
                if type(attr) != strongbox.linkset:
                    setattr(stub, name, getattr(data.private, name))
            stub.removeInjector(self.inject)
