# zdc.IdxDict - indexed dictionary

import UserDict

def _isNum(x):
    res = 0
    try:
        x = int(x)
        res = 1
    except:
        pass
    return res


class IdxDict(UserDict.UserDict):

    def __init__(self):
        UserDict.UserDict.__init__(self)
        self.idx = []

    def _toStringKey(self, key):
        """Convert numeric keys into string keys. Leaves string keys as is"""
        # handle numeric keys:
        if _isNum(key):
            if not (0 <= key < len(self.idx)):
                raise KeyError, `key` + " is out of bounds."
            # convert it to a string key
            key = self.idx[key]

        return key


    def __setitem__(self, key, item):
        key = self._toStringKey(key)
        
        # handle new string keys:
        if key not in self.idx:
            self.idx.append(key)

        self.data[key] = item


    def __getitem__(self, key):
        key = self._toStringKey(key)
        return self.data[key]
        
    def __repr__(self):
        res = "{"
        for key in self.idx:
            res = res + "'" + key + "': " + repr(self.data[key]) + ", "

        # strip that last comma and space:
        if len(res) > 1:
            res = res[:-2]

        res = res + "}"
        return res

    def keys(self):
        return self.idx
    

    #@TODO: what should __delitem__ do??
    # I'm not going to worry about it now, because
    # I don't need to delete anything from my lists.

