"""
Stealthbox: a strongbox that is not Observable
"""

from strongbox import attr, link, StrongboxError, linkset

class Accessorize(type):
    """
    Metaclass that automatically turns get_XXX and set_XXX into
    properties.
    """
    ## This is basically stolen from the 'autoprop' example
    ## in Guido's essay at http://www.python.org/2.2/descrintro.html
    def __init__(cls, name, bases, dict):
        super(Accessorize, cls).__init__(name, bases, dict)
        props = {}
        for name in dict.keys():
            if name.startswith("get_") or name.startswith("set_"):
                props[name[4:]] = 1
        for name in props.keys():
            fget = getattr(cls, "get_%s" % name, None)
            fset = getattr(cls, "set_%s" % name, None)
            setattr(cls, name, property(fget, fset))            

    
class Attributize(type):
    """
    Metaclass that adds __attrs__  member.
    __attrs__ works like __slots__ but uses static
    typing provided by the attr object.
    """
    def __init__(cls, name, bases, dict):
        super(Attributize, cls).__init__(name, bases, dict)
        cls.__attrs__ = {}
        for b in bases:
            if hasattr(b, "__attrs__"):
                cls.__attrs__.update(b.__attrs__)
        for name in dict.keys():
            if isinstance(dict[name], attr) and not name in cls.__attrs__:
                cls.__attrs__[name] = dict[name]
                delattr(cls, name)
        


class PrivateNamespace(object):
    """
    Just a normal python object.
    Instances are used for storing private variables.
    """
    pass


class StealthboxMetaclass(Accessorize, Attributize):
    pass
    

class Stealthbox(object):
    """
    Has everything in strongbox except its not observable.
    """
    __metaclass__=StealthboxMetaclass

    def __new__(klass, dbc=None, *args, **wargs):
        """
        set attributes to their defaults and creates the private namespace.
        """
        instance = object.__new__(klass)
        #@TODO: how do these two lines work with subclasses?
        #(maybe this is a job for setdefault?)
        instance.__dict__['private'] = PrivateNamespace()
        instance.__dict__['__values__'] = {}
        for a in klass.__attrs__:
            instance.__values__[a] = klass.__attrs__[a].initialValue()
        if dbc:
            instance.private.dbc = dbc
        return instance

    def __get_links__(klass):
        return [(k,v) for (k,v)
                in klass.__attrs__.items()
                if isinstance(v,link)]
    __get_links__ = classmethod(__get_links__)


    #@TODO: make these two into "__slots_of_type__(klass, type)"
    
    def __get_linksets__(klass):
        return [(k,v) for (k,v)
                in klass.__attrs__.items()
                if isinstance(v,linkset)]
    __get_linksets__ = classmethod(__get_linksets__)


    def __init__(self, **args):
        """
        This lets us initialize our attributes from the constructor.
        """
        self.private.isDirty = 1  # start out dirty so we get saved.
        self.update(**args)
        

    def update(self, **args):
        #@TODO: add "update" method to strongbox spec.
        for key in args:
            setattr(self, key, args[key])

    def __invalid(self, name):
        # complain when attribute is invalid. Note that
        # we can't use AttributeError because it breaks a
        # nested exception. For example,
        #     get_a(self): return self.b
        # when self.b doesn't exist.. With AttributeError,
        # it would give an error with "a" instead of with "b"
        # and I found that confusing.
        raise StrongboxError, \
              "'%s' is not a valid attribute for %s" \
              % (name, self.__class__.__name__)

    def __setattr__(self, name, value):
        # accessors
        if hasattr(self.__class__, name):
            try:
                getattr(self.__class__, name).__set__(self, value)
            except AttributeError, e:
                raise AttributeError("couldn't set %s to %s: %s"
                                     % (name, value, e))
        # attributes
        elif self.__values__.has_key(name):
            self.__values__[name] = self.__attrs__[name].sanitize(value)
        else:
            self.__invalid(name)
        self.private.isDirty = 1

    def __getattr__(self, name):
        if self.__values__.has_key(name):
            return self.__values__[name]
        else:
            self.__invalid(name)            

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__ ,
                           ", ".join(["%s=%s" % (k, repr(v)) for k,v in self.__values__.items()]))
