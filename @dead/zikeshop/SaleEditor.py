"""
SaleEditor - form editor for sales
"""
__ver__="$Id$"

import zikebase, zikeshop
zikebase.load("ObjectEditor")

class SaleEditor(zikebase.ObjectEditor):
    __super = zikebase.ObjectEditor
    whatClass = zikeshop.Sale

    def __init__(self, key=None, input=None):
        self.__super.__init__(self, self.whatClass, key, input)
        self._newData = {}
        for fld in self.object._links.keys():
            self._newData[fld] = {}

    def act_update(self):
        self.__super.act_update(self)

        #@TODO: move all this 1:* stuff into ObjectEditor itself.
        for item in self.input.keys():
            #@TODO: loop through whatClass._tuples:
            fld = "details"
            if (item[:len(fld)+1] == fld+"(") and (item[-1]==")"):
                # item should be in one of the following formats:
                #
                # fld{which|subfield}=value .. for existing 1:* joins
                # fld{+new|subfield}=value .. for new 1:* joins
                # @TODO: fld{+}=ID .. for linking w/ *:* joins 
                # @TODO: fld{-}=ID .. for unlinking w/ *:* joins 
                # @TODO: fld{subfield}  .. for 1:1 joins
                #
                meta = item[len(fld):]
                meta = meta[1:-1] # strip off {}
                import string
                meta = string.split(meta,"|")
                if len(meta)==2:
                    # this is a 1:* join
                    which, subfld = meta
                    # so figure out what kind of action it is (add, edit..)
                    if which[0]=="+":
                        # add a new record:
                        # actually, add to the _newData dictionary so we
                        # can add a new record later. We need to collect
                        # data on several fields first.
                        which = which[1:]
                        if not self._newData[fld].has_key(which):
                            # @TODO: make this an instance?
                            self._newData[fld][which]=\
                                getattr(self.object, fld).new()

                        setattr(self._newData[fld][which], subfld,
                                self.input[item])
                    else:
                        #@TODO: allow adding existing ID's, eg for *:* joins
                        #detail{+} maybe?
                        pass # edit existing record
                    
        # now actually add the data..
        for fld in self._newData.keys():
            for i in self._newData[fld].keys():
                getattr(self.object, fld) << self._newData[fld][i]
