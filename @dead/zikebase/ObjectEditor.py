"""
A class for editing zdc.Objects

$Id$
"""
import weblib

class ObjectEditor(weblib.Actor):
    """A class for editing descendents of zdc.Object"""  

    ## attributes ########################################

    whatClass = None # what class?
    object    = None # an instance of the class
    input  = {}

    ## constructor #######################################

    def __init__(self, what, key=None, input=None):
        """
        ex: ed=ObjectEditor(Person, aKey)
        or: ed=ObjectEditor(Person)
        or: ed=ObjectEditor(aParticularPersonInstance)

        In the first case, if aKey is None, a new object is created.
        This makes it handy for doing something like:

        ed = ObjectEditor(Person, weblib.request.get('ID'))
        """
        weblib.Actor.__init__(self, input)
        import types
        if type(what) == types.InstanceType:
            self.whatClass = what.__class__
            self.object = what
        else:
            self.whatClass = what
            if key:
                # get the instance based on the key:
                kFld = self.whatClass.__key__
                self.object = apply(self.whatClass, (), {kFld:key})
            else:
                # just make a new instance:
                self.object = self.whatClass()


    ## public methods ####################################

    def tuplize(self, input):
        if type(input) != type(()):
            return (input)
        else:
            return input
        
    def expected(self):
        """
        handles __expect__.. see test cases for docs..
        """
        import string
        res = {}
        __expect__ = self.input.get("__expect__", ())

        # it will either be a fieldname:value string...
        if type(__expect__) == type(""):
            field, value = string.split(__expect__, ":")
            res[field]=value
        # ... or a tuple of fieldname:value strings.
        else:
            for item in __expect__:
                field, value = string.split(item, ":")
                res[field] = value

        return res
        

    def parseCollections(self):
        #@TODO: further break this down, test, document..
        # new data for links, if used:
        self._newData = {}
        for fld in self.object.getEditableTuples():
            self._newData[fld] = {}
        ## @TODO: break these down into their own methods..
        ## this stuff lets you post multiple objects to a tuple
        ## (instead of just the IDs)... 
        for item in self.input.keys():
            #@TODO: loop through whatClass._tuples:
            for fld in self.object.getEditableTuples():
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




    def mergeTuples(self):
        """
        merge tuples (of IDs) into an object...
        it comes in handy for multi-select boxes and checboxes.
        """
        #@TODO: use the << notation..
        for field in self.object.getEditableTuples():
            if self.input.has_key(field):
                setattr(self.object, field, self.tuplize(self.input[field]))


    def mergeFields(self):
        """
        merge normal fields into the object
        """
        expected = self.expected()
        for field in self.object.getEditableAttrs():
            try:
                if self.input.has_key(field):
                    setattr(self.object, field, self.input[field])
                elif expected.has_key(field):
                    setattr(self.object, field, expected[field])
            except (ValueError, TypeError), err:
                self.errs.append(str(err))


    def mergeCollections(self):
        """
        merge collection data into the object..
        """
        #@TODO: this might not be the best way to factor this..
        #       note, however that zikeshop.SaleEditor overrides it.
        for fld in self._newData.keys():
            for i in self._newData[fld].keys():
                getattr(self.object, fld) << self._newData[fld][i]


    ## actions ###########################################

    def act_delete(self):
        self.object.delete()
        self.object = self.whatClass()
        

    def act_update(self):
        """
        update the object without saving it.
        """
        self.errs = []
        self.mergeFields()
        self.mergeTuples()
        self.parseCollections()
        self.mergeCollections()
        
        if self.errs:
            raise ValueError, self.errs

    def act_save(self):
        """
        updates the object and then saves it.
        """
        self.act_update()
        self.object.save()
