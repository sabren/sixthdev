
__ver__="$Id$"

import strongbox

class LinkInjector:
    def __init__(self, box, atr, clerk, fclass, fID):
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

        stub = fclass(ID=fID)
        setattr(box, atr, stub)
        stub.attach(self, onget="inject")


    def inject(self, stub, name):
        if name != "ID":
            data = self.clerk.fetch(self.fclass, self.fID)
            ## can't just call stub.update() because it
            ## was trying to assign linksets, which raises
            ## an AttributeError
            for name,attr in stub.__attrs__.items():
                ## @TODO: this doesn't seem very object-oriented. :/
                if type(attr) != strongbox.linkset:
                    setattr(stub, name, data.__values__[name])
            stub.detach(self)
