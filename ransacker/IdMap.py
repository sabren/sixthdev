"""
IdMap - maps keys to numbers and stores on disk.
"""
__ver__="$Id$"

import ransacker
import anydbm

class IdMap:

    def __init__(self, dict=None):
        if dict:
            self.data = dict
        else:
            self.data = {}
            

    def __getitem__(self, key):
        if self.data.has_key(key):
            return self.data[key]
        elif type(key) in (str, unicode):
            return self.__add(key)
        else:
            raise KeyError, "%s not found in IdMap" % key
        
        
    def __add(self, word):
        if self.data.has_key(word):
            raise KeyError, '"%s" is already in this Map.' % word
        else:
            newID = self.__nextID()
            self.data[word]=newID
            self.data[newID]=word
            return newID

    def __nextID(self):
        res = 1
        if self.data.has_key(ransacker.NEXTNUM):
            res = int(self.data[ransacker.NEXTNUM])
        self.data[ransacker.NEXTNUM] = str(res+1)
        return res

    def keys(self):
        """
        Returns all the keys except NEXTNUM
        """
        return [k for k in self.data.keys()
                if k is not ransacker.NEXTNUM]

    def has_key(self, key):
        return self.data.has_key(key)

    def __setitem__(self, name, value):
        raise KeyError, "cannot assign to IdMap"




