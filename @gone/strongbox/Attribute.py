"""
$Id$
"""
import sre
from types import StringType, LambdaType, ListType, NoneType

class Notgiven:
    "I'm a placeholder type distinct from None"

class Attribute(property):
    """
    A small class representing a static attribute.
    """
    def __init__(self, typ, okay=None, default=Notgiven, allowNone=1):
        self.type = typ
        self.allowNone = allowNone
        self._determineDefault(typ, default)
        self._setOkay(okay)

    def __repr__(self):
        return "#< %s = %s(%s, ...) >#" % (
            self.__name__,
            self.__class__.__name__,
            self.type.__name__,
        )
        
    def _setOkay(self, okay):
        if type(okay) == str:
            self.okay = sre.compile(okay)
        elif type(okay) in (LambdaType, ListType, NoneType):
            self.okay = okay
        else:
            raise TypeError, "okay must be lambda, list, or string"

    def initialValue(self, instance=None):
        """
        instance should be ignored, except for links
        #@TODO: make links a separate interface
        """
        return self.cast(self.default)

    def _determineDefault(self, typ, default):
        self.default = default
        if default is Notgiven:
            if typ == str:
                self.default = ''
            elif typ in (int, float, long):
                self.default = 0
            else:
                self.default = None
            
    def cast(self, value):
        if value is None:
            return None # str(None) returns 'None', so we need a special case.
        else:
            try:
                return self.type(value)
            except Exception, e:
                if value=="":
                    return None
                else:
                    raise TypeError, "%s: expected %s, got %s\n[%s]" \
                          % (value, self.type, type(value), e)

    def validate(self, value):
        if (value is None):
            return self.allowNone
        if self.okay is None:
            return 1
        elif type(self.okay)==LambdaType:
            return self.okay(value)
        elif type(self.okay)==ListType:
            return value in self.okay
        else:
            return self.okay.match(value) is not None
    
    def sanitize(self, value):
        if (self._typeok(value)) or (value is None):
            val = value
        else:
            val = self.cast(value)
        if not self.validate(val):
            raise ValueError, repr(value) + " vs " + repr(self.okay)
        return val # so the instance can store it


    def _typeok(self, value):
        """
        Factored out so I can override this in Link, etc.
        """
        return isinstance(value, self.type)

