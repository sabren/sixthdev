import zdc
import types
from strongbox import Strongbox

class RecordObject(Strongbox):
    """
    zdc.RecordObject - a simple Object that uses only one record for its data
    """
    __ver__="$Id$"


    ## static attributes ############################################

    _tablename = None
    _tuples = []
    __key__ = "ID"


    ## constructor ##################################################

    def __init__(self, ds, forceclerk=None,  **where):
        
        # make isclerk non-optional and you'll get
        # an error if it's not clerk (only for smoketest
        # while I'm refactoring this class out of existence)
        

        # ds turned out to be a bad idea.
        if ds:
            # you can do:
            # >>> obj = RecordObject(ds, tablename)
            #
            # OR you can define a class:
            #
            # >>> class Person(zdc.RecordObject):
            # >>>   _tablename = "mas_person"
            # >>>
            # >>> Person(ds)
            import warnings
            #raise "record objects should no longer use ds"
            #warnings.warn("record objects should no longer use ds")
            self.__dict__['_ds'] = ds
            self.__dict__['_table'] = zdc.Table(self._ds, self._tablename)

            # old-style compatability:
            self.__dict__['_data'] = self.__values__
            self.__dict__['_record'] = None

        if where:
            self._fetch(**where)
        else:
            self._new()

        # if all's well, go ahead with the init:
        super(RecordObject, self).__init__(**where)


    ## public methods ################################################
            
    def save(self):
        # save the contents of ._data into our record:
        # _data should always be the same data that's
        # stored in the database. 
        #
        # we do NOT put stuff in  __dict__!!!! 
        # __dict__ bypasses get_XXXXX and set_XXXXX !!)
        #
        # also, we must use _data rather than getattr
        # because getattr may by its very nature manipulate
        # the data (for example, a date may be stored internally
        # in one format, but set_thedate and get_thedate might
        # use another format altogether.
        #
        # The idea is that _data is private : no one else
        # messes with it, and therefore, it ENABLES rather
        # than breaks encapsulation.
        
        for f in self._table.fields:
            data = self._data[f.name] 
            if type(data) == types.InstanceType:
                # this is mostly for FixedPoints
                self._record[f.name] = str(data)
            else:
                self._record[f.name] = data
        self._record.save()
        

        # some fields may be calculated, so update our attributes:
        # use _data to avoid overhead/errors with setattr
        for f in self._table.fields:
            self._data[f.name] = self._record[f.name]


    #@TODO: test delete(), too...
    
    def delete(self):
        if getattr(self, self.__key__, None) is None:
            pass # nothing to delete
        else:
            self._record.delete()


    def getEditableAttrs(self):
        res = []
        for f in self._table.fields:
            res.append(f.name)
        return res


    def getEditableTuples(self):
        return self._tuples
        

    ## private methods ###############################################

    def _new(self):
        """
        Override this if you need to change behavior of new RecordObjects,
        for example, if a default value needs to be calculated rather than
        just assigned. BUT, make sure your new version calls this one or
        otherwise handles defaults.
        """
        self.__dict__['_record'] = zdc.Record(self._table)
        for f in self._record.table.fields:
            self._data[f.name] = None


    def _fetch(self, **where):
        """
        used internally to fetch a record...
        """
        self.__dict__['_record'] = self._table.fetch(**where)
        for f in self._record.table.fields:
            # use _data to avoid overhead/errors with setattr
            self._data[f.name] = self._record[f.name]

