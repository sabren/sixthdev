
class Observable(object):
    def __init__(self):
        self.observers = []
    def register(self, callback):
        self.observers.append(callback)
    def notify(self, source, event):
        for callback in self.observers:
            callback(source, event)
        
