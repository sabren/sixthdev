"""
strongbox: observable classes with accessors,
staticly typed attributes, and private namespaces
"""

from strongbox import Stealthbox

class Strongbox(Stealthbox):

    def __init__(self, **kwargs):
        self.private.observers = []
        super(Strongbox, self).__init__(**kwargs)
        
    def attach(self, observer, onset=None, onget=None):
        assert onset or onget
        self.private.observers.append((observer, onset, onget))

    def detach(self, observer):
        for row in self.private.observers:
            if row[0] is observer:
                self.private.observers.remove(row)

    def __notify__(self, event, name, value=None):
        assert event in ("set", "get")
        for row in self.private.observers:
            obs, onset, onget = row
            if (event == "set") and (onset is not None):
                getattr(obs, onset)(self, name, value)
            elif (event == "get") and (onget is not None):
                getattr(obs, onget)(self, name)
            
    def __setattr__(self, name, value):
        super(Strongbox, self).__setattr__(name, value)
        self.__notify__("set", name, value)

    def __getattr__(self, name):
        self.__notify__("get", name)
        return super(Strongbox, self).__getattr__(name)
