
class LinkSetInjector:
    def __init__(self, box, atr, clerk, fclass, fkey):
        self.clerk = clerk
        self.atr = atr
        self.fclass = fclass
        self.fkey = fkey
        box.attach(self, onget="inject")

    def inject(self, box, name):
        if name == self.atr:
            data = self.clerk.match(self.fclass, **{self.fkey:box.ID})
            for row in data:
                box.__values__[self.atr].append(row)
            box.detach(self)
