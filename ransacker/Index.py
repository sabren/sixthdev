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
import ransacker

class Index:

    ## attributes ##################################################

    rki = None
    wordHash = None


    ## constructor #################################################    

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
            # then assume it's the same name as the .rki
            rkw = rki[:-4] + ".rkw"

        self.rki = shelve.open(rki)
        self.wordHash = ransacker.WordHash(rkw)



    ## public methods ##############################################


    #- 1: methods that deal with page keys (k:/i:) ----------------#

    def hasPage(self, label):
        return self.rki.has_key("k:"+label)


    def addPage(self, label, text):
        """addPage(page, text) Add text to index under the given label"""
        assert type(label) == type(""), "label must be a string!"            

        if self.hasPage(label):
            self.unlinkPage(label)
        else:
            pageID = self.nextPageID()
            self.rki["i:"+`pageID`] = label
            self.rki["k:"+label] = (pageID, ())

        newWordIDs = []
        for word in ransacker.uniqueWords(text):
            self.linkPageToWord(label, word)
            newWordIDs.append(self.wordHash.get(word))

        pageData = [self.getPageID(label)] + newWordIDs
        self.rki["k:"+label] = pageData


    def getPageID(self, label):
        return self.rki["k:"+label][0]


    def wordIDsOnPage(self, label):
        return self.rki["k:"+label][1:]



    #- 2: methods that deal with wordID keys ----------------------#


    def unlinkPage(self, label):
        """If we know about a page, forget what we know about it."""
        # @TODO: check whether we NEED to delete (eg, word might be in new text)

        for wordID in self.wordIDsOnPage(label):
            pageIDs = list(self.pageIDsForWordID(wordID))
            pageIDs.remove(self.getPageID(label))
            self.rki[`wordID`]= pageIDs



    def linkPageToWord(self, label, word):
        wordID = self.wordHash.get(word)
        if self.rki.has_key(`wordID`):
            self.rki[`wordID`] = self.rki[`wordID`] + (self.getPageID(label),)
        else:
            self.rki[`wordID`] = (self.getPageID(label),)


    def pageIDsForWordID(self, wordID):
        return self.rki[str(wordID)]



    #- 3: methods that deal with other keys ------------------------#


    def nextPageID(self):
        res = 1
        if self.rki.has_key(ransacker.NEXTNUM):
            res = int(self.rki[ransacker.NEXTNUM])
        self.rki[ransacker.NEXTNUM] = str(res+1)
        return res



    ## magic methods ##############################################

    def __del__(self):
        self.rki.close()
        self.wordHash.close()







    ## this should be part of SearchEngine object ##########################

    def search(self, query):
        """Return a tuple of items that match query"""
        
        searchwords = string.split(query)
        hits = {}

        for word in searchwords:
            if self.wordHash.has_key(word):
                for item in self.rki[`self.wordHash[word]`]:
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



    ## this should go away ##################################################

    def index(self, key, text):
        self.addPage(key, text)
