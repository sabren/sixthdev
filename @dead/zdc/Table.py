"""
zdc.Table - a module representing a single table in a database.
"""
__ver__="$Id$"

import zdc
#@TODO: handle keys, defaults, autonumbers, etc..

class Table(zdc.Object):
    __super = zdc.Object

    ## attributes #############################################
    rowid = 'ID'  # set rowid to None if you don't use autonumber
    
    # @TODO: we need to know which module 'dbc' comes from, because
    # we need to get certain constants (eg, for field types)
    # that are in the module, but not connected to the
    # connection object... This is a shortcoming of the DB-API.. :/


    ## constructor ##############################################
                       
    def __init__(self, dbc, name):
        self.__super.__init__(self)
        self._data["dbc"] = dbc
        self._data["name"] = name
        self._data["fields"] = self._getFields()

    ## public methods ###########################################

    def getRecord(self, **where):
        return apply (zdc.Record, (self,), where)


    ## private methods ###########################################
       
    def _getFields(self):
        """Called internally to create .fields"""

        flds = zdc.IdxDict()
        # select a blank record:
        # @TODO: more sophisticated schema checking to get defaults, keys, etc?
        cur = self.dbc.cursor()
        cur.execute("SELECT * FROM " + self.name + " WHERE 1=0")
        for f in cur.description:
            flds[f[0]] = zdc.Field(f[0],               # name
                                   f[1],  #@TODO: make typeCode a string
                                   f[2],               # displaySize
                                   f[3],               # internalSize
                                   f[4],               # precision
                                   f[5],               # scale
                                   f[6],               # allowNull
                                   None)               # default
        return flds

