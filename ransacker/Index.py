"""
ransacker.indexer module

$Id$

this uses shelf to store data for a search engine.

rki is a ransacker index
rkw is a ransacker wordlist, mapping words to numeric ID's

rkw looks like: {
    NEXTNUM: 2,            # next ID to use
    "a":1}                 # the word "A"'s ID is 1

rki looks like: {
   NEXTNUM: 5,             # next ID to use
   "i:4": "Page4",         # item 4 has key "Page4"
   "k:Page4": (4, (1,)),   # key "Page4" is item 4, and contained word 1 ("a")
   "1": (4,) }             # word 1 ("a") was found on item 4

"""

import shelve
import string

NEXTNUM = "\t:nextnum"

class Index:

    def __init__(self, rki, rkw=None):
        """idx = ransacker.Index(rki, rkw=None)

        where:
        
           rki is the name of the index file (must end in .rki)
           rkw is the name of the word index (.rkw)

        if rkw is None, Index will use a file with
        the same name as the .rki, but with an .rkw extension.
        """
        
        assert rki[-4:]==".rki", "index filename must end in .rki"
        
        if rkw is None:
            rkw = rki[:-4] + ".rkw"

        self.rki = shelve.open(rki)
        self.rkw = shelve.open(rkw)

        if not self.rkw.has_key(NEXTNUM):
            self.rkw[NEXTNUM] = 1
        if not self.rki.has_key(NEXTNUM):
            self.rki[NEXTNUM] = 1
        


    def delKey(self, key):
        itemID, oldWordIDs = self.rki["k:"+key]

        # for each word in the index, remove the reference to this key.
        # @TODO: check whether we NEED to delete (eg, word might be in new text)
        for wordID in oldWordIDs:
            self.rki[`wordID`]= filter(lambda i,bad=itemID:i!=bad, self.rki[`wordID`])

        return self.rki["k:"+key][0]


    def addKey(self, key):
        """Adds a new key and returns the ItemID"""
        itemID = self.rki[NEXTNUM]
        self.rki[NEXTNUM] = itemID + 1
        self.rki["i:"+`itemID`] = key
        self.rki["k:"+key] = (itemID, ())
        return itemID



    def freqs(self, text):
        """Return a dict mapping words to frequencies"""
        fd = {}
        for word in string.split(text):
            if fd.has_key(word):
                fd[word] = fd[word] + 1
            else:
                fd[word] = 1
        return fd


    def newWordID(self):
        wordID = self.rkw[NEXTNUM]
        self.rkw[NEXTNUM] = self.rkw[NEXTNUM]+1
        return wordID
        


    def getWordID(self, word):
        # make sure the word is in the wordlist
        if not self.rkw.has_key(word):
            wordID = self.rkw[word] = self.newWordID()            
            # add a blank tuple in the index
            self.rki[`wordID`]=()
            return wordID
        else:
            return self.rkw[word]



    def index(self, key, text):
        """index(key, text) Add text to index and label it with the given key"""
        assert type(key) == type(""), "key must be a string!"            


        if self.rki.has_key("k:"+key):
            itemID = self.delKey(key)
        else:
            itemID = self.addKey(key)


        # now index
        newWordIDs = []
        for word in self.freqs(text).keys():
            # now add the reference
            wordID = self.getWordID(word)
            
            self.rki[`wordID`] = self.rki[`wordID`] + (itemID,)
            newWordIDs.append(wordID)

        self.rki["k:"+key] = tuple((self.rki["k:"+key][0], tuple(newWordIDs)))



    def search(self, query):
        """Return a tuple of items that match query"""
        
        searchwords = string.split(query)
        hits = {}

        for word in searchwords:
            if self.rkw.has_key(word):
                for item in self.rki[`self.rkw[word]`]:
                    if hits.has_key(item):
                        hits[item] = res[item]+1
                    else:
                        hits[item] = 1
                                    
            else:
                # this word wasn't found.
                pass


        # now we know the itemID's
        # next, lets sort by relevance
        res = hits.keys()
        res.sort(lambda a,b,h=hits: cmp(h[a],h[b]))
        
        
        # ... and turn the itemIDs into the corresponding alphanumeric keys
        for i in range(len(res)):
            res[i] = self.rki["i:"+`res[i]`]

        return tuple(res)



    def __del__(self):
        self.rki.close()
        self.rkw.close()


