
__ver__ = "$Id$"

class Observable(object):
    """
    From the 'Observer' design pattern from GoF book.
    """
    def __init__(self, **kwargs):
        self._ns().observers = []
        super(Observable, self).__init__(**kwargs)

    def _ns(self):
        """
        this is so strongbox can store observers in its
        private namespace.        
        """
        # do I really need this?
        return self

    def attach(self, observer, onset=None, onget=None):
        assert onset or onget
        self._ns().observers.append((observer, onset, onget))

    def detach(self, observer):
        for row in self._ns().observers:
            if row[0] is observer:
                self._ns().observers.remove(row)

    #@TODO: this doesn't need a magic name. "_notify" is fine.
    def __notify__(self, event, name, value=None):
        assert event in ("set", "get")
        for row in self._ns().observers:
            obs, onset, onget = row
            if (event == "set") and (onset is not None):
                getattr(obs, onset)(self, name, value)
            elif (event == "get") and (onget is not None):
                getattr(obs, onget)(self, name)
