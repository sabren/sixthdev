"""
zdc.Connection class - connects to a storage area.
"""
__ver__="$Id$"
import zdc

class Connection:

    def __init__(self, driver=None, **params):
        """
        driver should be a class or a string.
        """
        if driver:
            self.open(driver, **params)

    def cursor(self):
        return self.source.dbc.cursor()

    def open(self, driver, **params):
        self.source = driver

    # delegate everything else to the source...

    def select(self, tableOrClass , where=None, **wdict):
        import types
        if type(tableOrClass) in (types.ClassType, types.TypeType):
            tablename = tableOrClass._tablename
            res =  [tableOrClass (self, ID=row["ID"])
                    for row in self.source.select(tablename, where, **wdict)]
        else:
            tablename = tableOrClass 
            res = self.source.select(tablename, where, **wdict)
        return res

    def fields(self, tablename):
        return self.source.fields(tablename)

    def insert(self, tablename, data):
        return self.source.insert(tablename, data)

    def update(self, tablename, data, where=None, **wdict):
        return self.source.update(tablename, data, where, **wdict)

    def delete(self, tablename, where=None, **wdict):
        return self.source.delete(tablename, where, **wdict)
