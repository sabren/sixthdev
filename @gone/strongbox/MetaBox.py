"""
MetaBox: metaclass for strongbox
"""
from strongbox import BoxMaker       
       
class MetaBox(type):
    """
    This is a metaclass. It's used to build a
    new strongbox subclass, which can then be
    instantiated.

    For an overview of metaclasses, see:
    
        http://www.python.org/2.2/descrintro.html

    You should not use this class directly.
    Rather, subclass StrongBox.

    The real work of this metaclass is in BoxMaker.
    """
    def __new__(meta, name, bases, dict):
        """
        This is where we create the new class. 

        meta: always a reference to MetaBox (this class)
        name: the name of the class being defined
        bases: tuple of base classes
        dict: namespace with the 'class' contents (defs, attributes, etc)
        """
        return BoxMaker(meta, name, bases, dict).start()
    
    def __init__(klass, name, bases, dict):
        """
        now that we have the class, we can do stuff to it.
        in this case, we'll add accessor methods.

        same args as above, except now we get the
        class instead of the metaclass
        """
        super(MetaBox, klass).__init__(name, bases, dict)
        klass.maker.finish(klass)
