"""
ransacker.WordHash - maps words to numbers and stores on disk. (in a .rkw file)

$Id$
"""

import ransacker
import UserDict
import shelve

class WordHash(UserDict.UserDict):

    def __init__(self, filename):
        assert filename[-4:] == ".rkw", \
               "WordHash files must be named *.rkw"
        
        self.data = shelve.open(filename, "cf")
        
        if not self.data.has_key(ransacker.NEXTNUM):
            self.data[ransacker.NEXTNUM] = 1


    def get(self, word):
        try:
            res = self.add(word)
        except KeyError:
            res = self.data[word]
        return res


    def add(self, word):
        if self.data.has_key(word):
            raise KeyError, '"%s" is already in this hash.' % word
        else:
            self.data[word] = newID = self.newWordID()
            return newID


    def newWordID(self):
        wordID = self.data[ransacker.NEXTNUM]
        self.data[ransacker.NEXTNUM] = wordID+1
        return wordID      
    

    def close(self):
        self.data.close()


    def keys(self):
        """Returns all the keys except NEXTNUM"""
        return filter(lambda w: w[:2]!="\t:", self.data.keys())


    def __setitem__(self, name, value):
        raise KeyError, "cannot assign items to WordHash objects. use .get() or .add()"


    def __del__(self):
        self.data.close()



