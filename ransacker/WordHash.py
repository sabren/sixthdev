"""
ransacker.WordHash - maps words to numbers and stores on disk. (in a .rkw file)

$Id$


file format (disk-based hash):

 {NEXTNUM: 2,            # next ID to use
  "a":1}                 # the word "A"'s ID is 1

"""

import ransacker
import UserDict
import anydbm

class WordHash(UserDict.UserDict):

    def __init__(self, filename):
        assert filename[-4:] == ".rkw", \
               "WordHash files must be named *.rkw"
        
        self.data = anydbm.open(filename, "cf")


    def get(self, word):
        if self.data.has_key(word):
            return int(self.data[word])
        else:
            return self.add(word)


    def add(self, word):
        if self.data.has_key(word):
            raise KeyError, '"%s" is already in this hash.' % word
        else:
            newID = self.nextWordID()
            self.data[word] = str(newID)
            return newID


    def nextWordID(self):
        res = 1
        if self.data.has_key(ransacker.NEXTNUM):
            res = int(self.data[ransacker.NEXTNUM])
        self.data[ransacker.NEXTNUM] = str(res+1)
        return res

    

    def close(self):
        self.data.close()


    def keys(self):
        """Returns all the keys except NEXTNUM"""
        return filter(lambda w: w[:2]!="\t:", self.data.keys())


    def __setitem__(self, name, value):
        raise KeyError, "cannot assign items to WordHash objects. use .get() or .add()"


    def __del__(self):
        self.data.close()



