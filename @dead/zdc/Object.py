# zdc.Object
#
# a base class for building database objects


import Record

class Object:
    """A base class for building database objects.

    zdc.Object is a generic base class for manipulating
    records in a databae. It is intended to be used as a
    wrapper for one or more zdc.Record objects.

    see zikebase/linkwatcher for examples..
    """

    table = None
    locks = []
    
    
    def __init__(self, key=None, **kw):
        """Don't override this. override _new() or _fetch() instead."""
        self._isLocked = 0
        self._locks = self.__class__.locks[:]
        if key is None:
            if kw:
                apply(self.fetch, (), kw)
            else:
                self._new()
        else:
            self._fetch(key)
        self._lock()



    def _new(self):
        pass



    def _fetch(self, key=None, **kw):
        pass



    def _lock(self):
        self._isLocked = 1



    def save(self):
        pass



    def __setattr__(self, name, value):

        ## case A: there's a set_XXX method.
        if self.__class__.__dict__.has_key('set_' + name):
            self.__class__.__dict__['set_' + name](self, value)

        ## case B: object is locked, so be careful
        elif self.__dict__._isLocked:
            
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
        if self.__class__.__dict__.has_key('get_' + name):
            return self.__class__.__dict__['get_' + name](self)

        ## case B: the object has the attribute
        elif self.__dict__.has_key(name):
            return self.__dict__[name]

        ## case C: it does not have the attribute
        else:
            raise AttributeError, "no such attribute [" + name + "]"





