

class LinkSetInjector:
    def __init__(self, atr, clerk, fclass, fkey):
        """
        atr: the attribute name for the linkset
        clerk: a clerk
        fclass: the type of the linkset
        fkey: column name of the foreign key that points back to the parent
        """
        self.clerk = clerk
        self.atr = atr
        self.fclass = fclass
        self.fkey = fkey

    def inject(self, box, name):
        """
        box: the Strongbox instance we're being called from
        name: the attribute name that was getattr'd
        """
        if name == self.atr:
            table = self.clerk.schema.tableForClass(self.fclass)
            for row in self.clerk.storage.match(table, **{self.fkey:box.ID}):
                obj = self.clerk.rowToInstance(row, self.fclass)
                getattr(box.private, self.atr) << obj
            box.removeInjector(self.inject)
