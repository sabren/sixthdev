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


    ## actions ###########################################

    def act_delete(self):
        self.object.delete()
        self.object = self.whatClass()
        

    def act_update(self):
        '''
        update the object without saving it.
        '''
        import string
        
        expected = {}
        __expect__ = self.input.get("__expect__", ())
        if type(__expect__) == type(""):
            field, value = string.split(__expect__, ";")
            expected[field]=value
        else:
            # it's a tuple
            for item in __expect__:
                field, value = string.split(item, ";")
                expected[field] = value

        errs = []
        for field in self.object.getEditableAttrs():
            try:
                if self.input.has_key(field):
                    setattr(self.object, field, self.input[field])
                elif expected.has_key(field):
                    setattr(self.object, field, expected[field])
            except (ValueError, TypeError), err:
                errs.append(str(err))

        #@TODO: get rid of editable tuples, or add __expect__
        for field in self.object.getEditableTuples():
            if self.input.has_key(field):
                setattr(self.object, field, self.tuplize(self.input[field]))

        if errs:
            raise ValueError, errs

    def act_save(self):
        '''
        updates the object and then saves it.
        '''
        self.act_update()
        self.object.save()
