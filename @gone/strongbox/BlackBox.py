from strongbox import MetaBox, Private

# I thought about factoring out a
# BaseBox... But I just couldn't
# think of a difference, and I like
# the name BlackBox better. 

class BlackBox(object):
    __metaclass__ = MetaBox
    
    def __init__(self, **kwargs):
        self.__private__()
        for slot, attr in self.__attrs__.items():
            setattr(self.private, slot, attr.initialValue(self))
        self.update(**kwargs)

    def __private__(self):
        self.private = Private()        

    def update(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def onSet(self, slot, value):
        pass

    def onGet(self, slot):
        pass

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__ ,
                           ", ".join(["%s=%s" % (a, getattr(self, a))
                                      for a in self.__attrs__]))
