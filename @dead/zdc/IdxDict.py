"""
an indexed dictionary (cross between list and dict)
"""
__ver__="$Id$"
import UserDict

class IdxDict(UserDict.UserDict):
    __super = UserDict.UserDict

    def __init__(self):
        self.__super.__init__(self)
        self.idx = []

    def _toStringKey(self, key):
        """Convert numeric keys into string keys. Leaves string keys as is"""
        # handle numeric keys:
        if type(key)==type(0):
            if not (0 <= key < len(self.idx)):
                ## oddly enough, it is this IndexError here
                ## that allows you to do "for x in myIdxDict:"
                raise IndexError, `key` + " is out of bounds."
            # convert it to a string key
            key = self.idx[key]
        return key


    def __setitem__(self, key, item):
        """
        we can only use a numeric key if it's bigger than
        the length of the index..
        
        eg,after:
        >>> idx['a'] = 'abc'
        idx[0] now maps to "a", so:
        >>> idx[0] = 'xyz'
        is a reassignment. BUT:
        >>> idx[1] = 'efg'
        is a normal assignment.

        To handle the magic of figuring out the last index, use 'append':

        >>> idx.append('hijk')
        >>> idx.keys()
        ['a', 1, 2]
        >>> idx[2]
        'hijk'
        """
        
        if (type(key) == type(0)) and (key < len(self.idx)):
            key = self._toStringKey(key)
                
        if not key in self.idx:
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

    #### these are so we can treat it like its a list ######
    def __len__(self):
        return len(self.idx)

    def clear(self):
        self.__super.clear(self)
        self.idx = []
    
    def __getslice__(self, i, j):
        i = max(i, 0); j = max(j, 0)
        res = []
        for item in self.idx[i:j]:
            res.append(self.data[item])
        return res

    def append(self, other):
        self[len(self.idx)]=other
    
    ### .. or like a dictionary: #########
    def keys(self):
        return self.idx

    def values(self):
        return self[:]

    ### << is a magical append operator ##########
    def __lshift__(self, other):
        self.append(other)

    #@TODO: what should __delitem__ do??
    # I'm not going to worry about it now, because
    # I don't need to delete anything from my lists.
