## zdc.RecordObject 

import zdc.Object

class RecordObject(zdc.Object):

    table = None
    defaults = {}

    def __init__(self, dbc, table=None, defaults=None):

        # you can do obj = RecordObject(dbc, sometable)
        #
        # OR you can define a class:
        #
        # class Person(dbc):
        #    table = "mas_person"
        
        if table:
            self.table = table
        else:
            self.table = self.__class__.table

        assert self.table is not None, "RecordObjects must have a table."


        # same thing with the defaults, except they're optional
        
        if defaults:
            self.defaults = defaults
        else:
            self.defaults = self.__class__.defaults



        # if all's well, go ahead with the init:
        zdc.Object.__init__(self, dbc)


    def _new(self):
        rec = zdc.Record(self.dbc, self.table)
        for f in rec.fields:
            if self.defaults.has_key(f.name):
                setattr(self, f.name, self.defaults[f.name])
            else:
                setattr(self, f.name, None)


    #@TODO: TEST THIS - it was just an off-the-top-of-my-head thing

    def _fetch(self, key):
        rec = zdc.Record(self.dbc, self.table)
        rec.fetch(key)
        for f in rec.fields:
            setattr(self, f.name, rec[f.name])

            
    def save(self):
        rec = zdc.Record(self.dbc, self.table)
        for f in rec.fields:
            rec[f.name] = getattr(self, f.name)
        rec.save()
        for f in rec.fields:
            setattr(self, f.name, rec[f.name])
