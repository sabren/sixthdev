"""
BoxMaker: the brains behind MetaBox
"""
from strongbox import attr

class BoxMaker(object):
    """
    This is where the real work of MetaBox is done.
    It's just a normal object that builds a class.
    
    I separated it out because I wanted to hold
    some state information through the various
    phases of building the class:

    There are three passes:

       1. MetaBox.__new__ calls BoxMaker.start()
          which returns a new class
          
       2. MetaBox.__init__ calls BoxMaker.finish()
          which adds some magic property accesors

       3. StrongBox.__init__() then does some
          perfectly normal intitialization stuff
       
    """
    def __init__(self, type, name, bases, dict):
        self.type = type
        self.name = name
        self.bases = bases
        self.dict = dict
        self.attrs = [a for a in dict if isinstance(dict[a], attr)]

        self.addSlots()
        self.addAttrs()

    ## first pass (__new__): ################################

    def start(self):
        klass = type.__new__(self.type, self.name, self.bases, self.dict)
        klass.maker = self
        return klass

    def addSlots(self):
        slots = ["private"]
        for a in self.attrs:
            slots.append(a)
        self.dict["__slots__"] = slots

    def addAttrs(self):
        """
        this is really just for backwards compatability
        """
        attrs = {}
        for b in self.bases:
            if hasattr(b, "__attrs__"):
                attrs.update(b.__attrs__)
        for a in self.attrs:
            attrs[a] = self.dict[a]
            attrs[a].__name__ = a
        self.dict["__attrs__"] = attrs

    ## second pass (__init__) ###############################

    def finish(self, klass):
        self.addAccessors(klass)
        self.addAttrOwners(klass)

    def addAttrOwners(self, klass):
        for a in self.attrs:
            getattr(klass, a).__owner__ = klass

    def makeGetter(self, klass, slot):
        def getter(instance):
            instance.onGet(slot)
            return getattr(instance.private, slot)
        return getter

    def makeSetter(self, klass, slot):
        def setter(instance, val):
            val = getattr(klass, slot).sanitize(val)
            setattr(instance.private, slot, val)
            instance.onSet(slot, val)
        return setter
        
    def addAccessors(self, klass):
        props = {}
        
        # first get all the attributes:
        for a in self.attrs:
            props[a] = self.dict[a]

        # next, the getters and setters:
        getter = {}
        setter = {}
        for item in self.dict:
            slot = item[4:]
            if item.startswith("get_"):
                getter[slot] = self.dict[item]
            elif item.startswith("set_"):
                setter[slot] = self.dict[item]
            else:
                continue
            props.setdefault(slot, property())

        # now make the accessors:
        for slot in props:
            prop = props[slot]
            
            fget = getter.get(slot)
            if (slot in self.attrs) and (not fget):
                fget = self.makeGetter(klass, slot)
                
            fset = setter.get(slot)
            if (slot in self.attrs) and (not fset):
                fset = self.makeSetter(klass, slot)

            # this is the only way you can set .fget and .fset:
            property.__init__(prop, fget, fset)
            setattr(klass, slot, prop)
