"""
strongbox: observable classes with accessors,
staticly typed attributes, and private namespaces
"""

from strongbox import attr

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
    Metaclass that adds a __attrs__ member.
    __attrs__ works like __slots__ but uses static
    typing provided by the attr object.
    """
    def __init__(cls, name, bases, dict):
        super(Attributize, cls).__init__(name, bases, dict)
        cls.__attrs__ = {}
        for name in dict.keys():
            if isinstance(dict[name], attr):
                cls.__attrs__[name] = dict[name]
                delattr(cls, name)
                del dict[name]


class PrivateNamespace(object):
    """
    Just a normal python object.
    Instances are used for storing private variables.
    """
    pass


class StrongboxMetaclass(Accessorize, Attributize):
    pass
    

class Strongbox(object):
    """
    A strongly typed 
    """
    __metaclass__=StrongboxMetaclass

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
            default = klass.__attrs__[a].default
            instance.__values__[a] = klass.__attrs__[a].cast(default)
        if dbc:
            instance.private.dbc = dbc
        return instance

    def __init__(self, **args):
        """
        This lets us initialize our attributes from the constructor.
        """
        self.update(**args)

    def update(self, **args):
        #@TODO: add "update" method to strongbox spec.
        for key in args:
            setattr(self, key, args[key])

    def __invalid(self, name):
        raise AttributeError, \
              "'%s' is not a valid attribute for %s" \
              % (name, self.__class__.__name__)

    def __setattr__(self, name, value):
        # accessors
        if hasattr(self.__class__, name):
            getattr(self.__class__, name).__set__(self, value)
        # attributes
        elif self.__values__.has_key(name):
            self.__values__[name] = self.__attrs__[name].sanitize(value)
        else:
            self.__invalid(name)

    def __getattr__(self, name):
        # attributes
        if self.__values__.has_key(name):
            return self.__values__[name]
        else:
            self.__invalid(name)            


class ObservableStrongbox(Strongbox):
    """
    'Subject' from the GoF Observer pattern.
    """
    def __init__(self):
        self.private.observers = []
    def attach(self, observer):
        self.private.observers.append(observer)
    def detach(self, observer):
        self.private.observers.remove(observer)
    def notify(self):
        for observer in self.private.observers: observer.update(self)


