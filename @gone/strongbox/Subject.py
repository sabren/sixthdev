
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
