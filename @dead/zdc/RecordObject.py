"""
zdc.RecordObject - a simple Object that uses only one record for its data

$Id$
"""

import zdc.Object

#@TODO: there ought to be a validateKey method, for passing in keywords as keys..
#@TODO: maybe we don't need the concept of a 'key' parameter at all..


class RecordObject(zdc.Object):

    ## attributes ###################################################

    _table = None
    _defaults = {} # perhaps just check whether __class__.attr is defined?
    _record = None


    ## constructor ##################################################

    def __init__(self, _table=None, _defaults=None, **where):
        # you can do obj = RecordObject(table)
        #
        # OR you can define a class:
        #
        # class Person(zdc.RecordObject):
        #    _table = "mas_person"
        
        if _table:
            self._table = _table
        assert self._table is not None, "RecordObjects must have a table."

        # same thing with the defaults, except they're optional       
        if _defaults:
            self._defaults = _defaults

        # if all's well, go ahead with the init:
        apply (zdc.Object.__init__, (self, self._table.dbc), where)


    ## public methods ################################################
            
    def save(self):
        # save the data in our record:
        for f in self._table.fields:
            self._record[f.name] = getattr(self, f.name)
        self._record.save()

        # some fields may be calculated, so update our attributes:
        # use __dict__ to avoid overhead/errors with setattr
        for f in self._table.fields:
            self.__dict__[f.name] = self._record[f.name]


    #@TODO: test delete(), too...
    
    def delete(self):
        if self.isNew:
            pass # nothing to delete
        else:
            self._record.delete()


    ## private methods ###############################################

    def _new(self):
        self._record = zdc.Record(self._table)
        for f in self._record.table.fields:
            
            # populate with default values.
            # use __dict__ to avoid overhead/errors with setattr
            if self._defaults.has_key(f.name):
                self.__dict__[f.name] =  self._defaults[f.name]
            else:
                self.__dict__[f.name] = None


    #@TODO: TEST THIS - it was just an off-the-top-of-my-head thing

    def _fetch(self, **where):
        self._record = apply(zdc.Record, (self._table,), where)
        for f in self._record.table.fields:
            # use __dict__ to avoid overhead/errors with setattr
            self.__dict__[f.name] = self._record[f.name]




