"""
zdc.Connection class - connects to a storage area.
"""
__ver__="$Id$"

class Connection:
    from MySQLdb import * # for NUMBER, etc..

    def __init__(self, driver=None, **params):
        if driver:
            apply(self.open, (driver,), params)

    def cursor(self):
        return self.source.dbc.cursor()

    def open(self, driver, **params):
        self.source = driver

    # delegate everything to the source...

    def select(self, tablename, where=None, **wdict):
        return apply(self.source.select, (tablename, where), wdict)

    def fields(self, tablename):
        return self.source.fields(tablename)

    def insert(self, tablename, data):
        return self.source.insert(tablename, data)

    def update(self, tablename, data, where=None, **wdict):
        return apply(self.source.update, (tablename, data, where), wdict)


    def delete(self, tablename, where=None, **wdict):
        return apply(self.source.delete, (tablename, where), wdict)
