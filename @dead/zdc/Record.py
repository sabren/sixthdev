"""
zdc.Record -  makes it easy to edit records in a database.
"""
__ver__="$Id$"

import zdc
import UserDict

class Record(UserDict.UserDict):

    ## class attributes ##########################################

    table = None

    ## constructor ###############################################

    def __init__(self, table=None, **data):

        ## we're a new instance by default..
        self.isNew = 0

        ## A record's table can be passed in the constructor or
        ## defined a subclass's definition... Most likely, you won't
        ## create records directly, but call someTable.fetch(key)
        
        if table:
            self.table = table
        assert self.table is not None, "Record must have an associated Table!"

        # a hack for initial timestamping. @TODO: clean this up!
        self.insertStamps = []

        # populate the data.. you probably don't want to do this,
        # either.. Rather, go through Table.
        self.data = zdc.IdxDict()
        if data:
            self.data.update(data)
        else:
            self._new()


    ## public methods ###############################################

    def delete(self):
        """
        Deletes the record.
        """
        self.table.delete(self[self.table.rowid])

    def save(self):
        """
        Inserts or Updates the record.
        """
        if self.isNew:
            self._insert()
            self.isNew = 0
        else:
            self._update()


    ## private methods #################################################

    def _new(self):
        """
        Prepare to add a new record. This is called by default.
        """
        self.isNew = 1
        for f in self.table.fields:
            self.data[f.name] = f.default

    def _update(self):
        """
        called when saving a record that's already in the table.
        """
        self.table.update(self[self.table.rowid], self)

    def _insert(self):
        """
        calld when saving a record that's not already in the table.
        """
        self.table.insert(self)

