

class ObjectEditor:
    """A class for editing descendents of zdc.Object"""

    ## attributes ########################################

    what   = None # what class?
    object = None # an instance of the class
    input  = {}

    ## constructor #######################################

    def __init__(self, what, **args):
        """ex: objed=ObjectEditor(Person, fName="fred", lName="smith")"""
        self.what = what
        self.object = apply(self.newObject, (), args)


    ## public methods ####################################

    def newObject(self, **which):
        """Create a new instance of whatever class we're editing."""
        
        ## this next bit is python magic that will
        ## create a "what" and pass "where" to the
        ## constructor, assigning the result to self.object
        ##
        ## in the example above, objed.object would be
        ## a Person object representing "fred smith".
        
        return apply(self.what, (), which)


    def act(self, input):
        """objed.act(input) #input=a dict with a key called 'action'."""

        self.input = input
        if input.has_key("action"):
            method = "act_" + input["action"]

            ## more python magic to call the method:
            if hasattr(self, method):
                apply(getattr(self, method), ())
            else:
                raise "Don't know how to %s!" % action

        else:
            pass # do nothing - no action given


    def tuplize(self, input):
        if type(input) != type(()):
            return (input)
        else:
            return input


    ## actions ###########################################

    def act_delete(self):
        self.object.delete()
        self.object = self.newObject()
        

    def act_save(self):
        for field in self.object.getEditableAttrs():
            if self.input.has_key(field):
                setattr(self.object, field, self.input[field])
        for field in self.object.getEditableTuples():
            if self.input.has_key(field):
                setattr(self.object, field, self.tuplize(self.input[field]))
        self.object.save()

