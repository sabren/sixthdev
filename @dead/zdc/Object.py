"""
zdc.Object - a base class for building database objects
"""
__ver__ = "$Id$"

import Record

class Object:
    """
    A base class for building business objects.

    zdc.Object is a generic base class for business
    objects. It has the ability to reject adding
    attributes that don't apply to it.

    see RecordObject and ModelObject (?) for examples..
    """

    __key__="ID" # field that uniquely identifies this object
    _links = {}
    _locks = []
    
    def __init__(self, key=None, **where):
        """
        Don't override this! override _init(), _new() or _fetch() instead.
        """
        self.__dict__['_data']={}
        self._link()
        self._init()

        if key is None:
            if where:
                apply(self._fetch, (), where)
            else:
                self._new()
        else:
            self._fetch(key)
        self._lock()



    ### Abstract Protected Methods ##########################

    def _link(self):
        """
        Set up the links (relationships) between the objects.
        This is pretty generic, so you probably don't need to
        override it. Just populate class._links.

        Structure is:

        _links = {
           collectionName : (linkClass, params, to, linkClass's, constructor)
        }

        linkclasses (eg, zdc.LinkSet) Should take the left-hand object
        (self, from our perspective) as the first parameter. You don't
        have to include self in the param list.

        eg:

        _links = {
           'details': (zdc.LinkSet, SomeDetailClass, 'ID', 'summaryID')
        }
        """
        for item in self._links.keys():
            setattr(self, item, apply(self._links[item][0],
                                      (self,) + tuple(self._links[item][1:])))

        
    def _init(self):
        """
        Override this to initialize an Object before
        the data is filled in by _new or _fetch.
        """
        pass
    

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


    def getEditableTuples(self):
        raise NotImplementedError, "Object.getEditableTuples()"


    ### private Methods ####################################


    def get__isLocked(self):
        """
        Makes sure we're unlocked by default.
        
        we can't put this in __init__ because child classes
        might want to do stuff before calling _new() or _save()
        and therefore, before __init__..
        """
        
        if not self.__dict__.has_key("isLocked"):
            self.__dict__["isLocked"] = 0
        return self.__dict__["isLocked"]


    def _findmember(self, member):
        """
        self._findmember(member) : does self define or inherit member?

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

            ## B2: editable object attribute
            elif self._data.has_key(name):
                self._data[name] = value

            ## B3: normal python attribute:
            elif self.__dict__.has_key(name):
                self.__dict__[name] = value
                
            ## B4: Attribute isn't part of the object
            else:
                raise AttributeError, \
                      "can't add new attributes to locked object."

        ## case C: unlocked, so do whatever you want
        else:
            self.__dict__['_data'][name] = value
        


    def __getattr__(self, name):

        ## case A: the name is already in __dict__
        ## python (1.52 anyway) won't call __getattr__,
        ## and there's not a damn thing we can do about it.

        ## case B: there's a get_XXX method:
        meth = self._findmember('get_' + name)
        if meth is not None:
            return meth(self)

        ## case C: the attribute is in _data
        elif self._data.has_key(name):
            return self._data[name]

        ## case D: it does not have the attribute
        else:
            raise AttributeError, "no such attribute [" + name + "]"
