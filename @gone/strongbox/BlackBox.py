from strongbox import MetaBox, Private, Attribute

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
        # for linksets and in other cases where objects refer
        # back to each other, this could create an infinite loop,
        # so we only show plain attributes.
        return "%s(%s)" % (self.__class__.__name__ ,
                           ", ".join(["%s=%s" % (a, getattr(self, a))
                                      for a,v in self.__attrs__.items()
                                      if v.__class__ is Attribute]))
    

##    ## this stuff is for pickling... but it turns out pickling
##    ## is a can of worms when you have injectors lying around.
##    ## I think maybe you can use pickle OR clerk but not both.
##    ## I haven't tested that theory though.
##   
##     def memento(self):
##         res = {}
##         for a in self.__attrs__:
##             res[a]=getattr(self,a)
##         return res
##     def __getstate__(self):
##         return self.memento()
##     def __setstate__(self, memento):
##         self.__private__()
##         self.update(**memento)
