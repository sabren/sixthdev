

class LinkInjector:
    def __init__(self, box, atr, sto, fclass, fID):
        """
        Registers a callback so that when getattr(box, atr)
        is called, the object of box.atr's type with given ID
        is loaded from sto and injected into box.

        In other words, this provides lazy loading for
        strongboxen.
        """

        self.storage = sto
        self.fID = fID
        self.fclass = fclass

        stub = fclass(ID=fID)
        setattr(box, atr, stub)
        stub.attach(self, onget="inject")


    def inject(self, stub, name):
        if name != "ID":
            data = self.storage.fetch(self.fclass, self.fID)
            stub.update(**data.__values__)
            stub.detach(self)
