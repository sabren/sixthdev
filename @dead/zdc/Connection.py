"""
zdc.Connection class - connects to a storage area.
"""
__ver__="$Id$"
import zdc

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

    def select(self, table, where=None, **wdict):
        #@TODO: clean this up and test it!
        import types
        if type(table) == types.ClassType:
            tablename = table._table.name
            res =  map(lambda row, klass=table: klass(ID=row["ID"]),
                       apply(self.source.select, (tablename, where), wdict))
        else:
            tablename = table
            res = apply(self.source.select, (tablename, where), wdict)
        return res

    def fields(self, tablename):
        return self.source.fields(tablename)

    def insert(self, tablename, data):
        return self.source.insert(tablename, data)

    def update(self, tablename, data, where=None, **wdict):
        return apply(self.source.update, (tablename, data, where), wdict)


    def delete(self, tablename, where=None, **wdict):
        return apply(self.source.delete, (tablename, where), wdict)
