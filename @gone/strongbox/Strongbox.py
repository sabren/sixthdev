
from strongbox import Stealthbox, Observable

class Strongbox(Observable, Stealthbox):
    """
    strongbox: observable classes with accessors,
    staticly typed attributes, and private namespaces
    """

    def __init__(self, **kwargs):
        super(Strongbox, self).__init__(**kwargs)

    def _ns(self):
        """
        Overrides Observable._ns() to use private namespace.
        """
        return self.private
        
    def __setattr__(self, name, value):
        super(Strongbox, self).__setattr__(name, value)
        self.__notify__("set", name, value)

    def __getattr__(self, name):
        self.__notify__("get", name)
        return super(Strongbox, self).__getattr__(name)
