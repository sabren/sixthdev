"""
zdc.Table - a module representing a single table in a database.

$Id$
"""
import zdc


#@TODO: handle keys, defaults, autonumbers, etc..


class Table:

    ## attributes #############################################

    name = ""
    fields = {}
    rowid = 'ID'  # set rowid to None if you don't use autonumber
    
    # we need to know which module 'dbc' comes from, because
    # we need to get certain constants (eg, for field types)
    # that are in the module, but not connected to the
    # connection object... This is a shortcoming of the DB-API.. :/

    dbc = None
    dbc_module = None
    

    ## constructor ##############################################
                       
    def __init__(self, dbc, name, module=None, rowid=''):
        self.dbc = dbc
        self.name = name
        self.fields = self._getFields()


        if rowid != '':
            self.rowid = rowid


        # Not all DB-API modules have a __class__.__module__
        # so we're forced to guess..
        # @TODO: a better way to guess the dbc's module
        
        if module:
            self.module = module
        else:
            try:
                mod = dbc.__class__.__module__
                exec('import ' + mod)
                self.dbc_module = eval(mod)
            except:
                raise "Couldn't guess DB-API module. Pass 'module' parameter to Table()"



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

