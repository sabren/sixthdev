"""
strongbox: observable classes with accessors,
staticly typed attributes, and private namespaces
"""

from strongbox import Stealthbox

class Strongbox(Stealthbox):
    def __init__(self, **kwargs):
        super(Strongbox, self).__init__(**kwargs)
        self.private.observers = []
    def attach(self, observer):
        self.private.observers.append(observer)
    def detach(self, observer):
        self.private.observers.remove(observer)
    def notify(self):
        for observer in self.private.observers: observer.update(self)


