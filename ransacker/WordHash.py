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
        # make sure the word is in the wordlist
        if not self.data.has_key(word):
            wordID = self.data[word] = self.newWordID()
            return wordID
        else:
            return self.data[word]

    

    def newWordID(self):
        wordID = self.data[ransacker.NEXTNUM]
        self.data[ransacker.NEXTNUM] = self.data[ransacker.NEXTNUM]+1
        return wordID      
    


    def close(self):
        self.data.close()
    
