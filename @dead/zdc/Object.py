# zdc.Object
#
# a base class for building database objects


import Record

class Object:
    """A base class for building database objects.

    zdc.Object is a generic base class for manipulating
    records in a databae. It is intended to be used as a
    wrapper for one or more zdc.Record objects.

    see RecordObject and ModelObject (?) for examples..
    """

    locks = []
    isNew = 0

    
    def __init__(self, dbc, key=None, **where):
        """Don't override this. override _new() or _fetch() instead."""

        self._locks = self.__class__.locks[:]
        self.dbc = dbc

        self.isNew = not ((key) or (where))

        if key is None:
            if where:
                apply(self._fetch, (), where)
            else:
                self._new()
        else:
            self._fetch(key)
        self._lock()



    ### Abstract Protected Methods ##########################

    def _new(self):
        raise NotImplementedError, "Object._new()"



    def _fetch(self, key=None, **kw):
        raise NotImplementedError, "Object._fetch()"



    def _lock(self):
        self._isLocked = 1


    ### Abstract Public Methods ############################

    def save(self):
        raise NotImplementedError, "Object.save()"


    def delete(self):
        raise NotImplementedError, "Object.delete()"


    def getEditableAttrs(self):
        raise NotImplementedError, "Object.getEditableAttrs()"


    ### private Methods ####################################


    def get__isLocked(self):
        """Makes sure we're unlocked by default.
        
        we can't put this in __init__ because child classes
        might want to do stuff before calling _new() or _save()
        and therefore, before __init__..
        """
        
        if not self.__dict__.has_key("isLocked"):
            self.__dict__["isLocked"] = 0
        return self.__dict__["isLocked"]


    def _findmember(self, member):
        """self._findmember(member) : does self define or inherit member?

        with subclasses, It's hard to tell if we have get_XXX,
        because we have to iterate through all the base classes.
        This ought to be built in to python, but it isn't.. :/
        """

        res = None

        # __bases__ is only the IMMEDIATE parent, so we have
        # to climb the tree...        
        #@TODO: handle multiple inheritence
        ancestors = [self.__class__]
        while ancestors[-1].__bases__ != ():
            ancestors.append(ancestors[-1].__bases__[0])
        
        for ancestor in ancestors:
            for item in dir(ancestor):
                if item == member:
                    res = ancestor.__dict__[member]
                    break

        return res
        

    def __setattr__(self, name, value):
        

        ## case A: there's a set_XXX method.
        meth = self._findmember('set_' + name)
        if meth is not None:
            meth(self, value)

        ## case B: object is locked, so be careful
        elif self._isLocked:
            
            ## B1: locked (read only) attribute
            if name in self._locks:
                raise AttributeError, name + " is read-only."

            ## B2: normal (editable) attribute
            elif self.__dict__.has_key(name):
                self.__dict__[name] = value

            ## B3: Attribute isn't part of the object
            else:
                raise AttributeError, "can't add new attributes to locked object."

        ## case C: unlocked, so do whatever you want
        else:
            self.__dict__[name] = value
        


    def __getattr__(self, name):

        ## case A: there's a get_XXX method:
        meth = self._findmember('get_' + name)
        if meth is not None:
            return meth(self)


        ## case B: the object has the attribute
        elif self.__dict__.has_key(name):
            return self.__dict__[name]

        ## case C: it does not have the attribute
        else:
            raise AttributeError, "no such attribute [" + name + "]"





