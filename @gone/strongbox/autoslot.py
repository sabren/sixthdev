
def AutoSlotMaker(name, bases, dict):
    import pdb; pdb.set_trace()
    d = {}
    d.update(dict)
    d["__slots__"]=("a","b","c")
    return type(name, bases, d)


class AutoSlot(object):
    __metaclass__=AutoSlotMaker
    def __call__(self, name, bases, dict):
        print "in here"

class Aha(AutoSlot):
    pass



as = AutoSlot()
ah = Aha()

