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

import anydbm
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

        self.rki = anydbm.open(rki, "cf")
        self.wordHash = ransacker.WordHash(rkw)



    ## public methods ##############################################


    def hasLabel(self, label):
        return self.rki.has_key("k:"+label)

    def getLabel(self, pageID):
        return self.rki["i:"+`pageID`]


    def addPage(self, label, text):
        """addPage(page, text) Add text to index under the given label"""
        assert type(label) == type(""), "label must be a string!"            

        if self.hasLabel(label):
            self.unlinkPage(label)
            pageID = self.getPageID(label)
        else:
            pageID = self.nextPageID()
            self.rki["i:"+`pageID`] = label


        wordIDs = []
        for word in ransacker.uniqueWords(text):
            wordID = self.wordHash.getID(word)
            wordIDs.append(wordID)
            
            pageIDs = []
            if self.rki.has_key(str(wordID)):
                pageIDs = self.pageIDsForWordID(wordID)

            pageIDs.append(pageID)
            self.rki[str(wordID)] = ransacker.intListToStr(pageIDs)


        self.rki["k:"+label] = ransacker.intListToStr([pageID] + wordIDs)


    def getPageID(self, label):
        return ransacker.strToIntList(self.rki["k:"+label])[0]



    def wordIDsOnPage(self, label):
        return ransacker.strToIntList(self.rki["k:"+label])[1:]


    def unlinkPage(self, label):
        """If we know about a page, forget what we know about it."""
        # @TODO: check whether we NEED to delete (eg, word might be in new text)

        for wordID in self.wordIDsOnPage(label):
            pageIDs = self.pageIDsForWordID(wordID)
            pageIDs.remove(self.getPageID(label))
            self.rki[`wordID`]= ransacker.intListToStr(pageIDs)


    def pageIDsForWordID(self, wordID):
        return ransacker.strToIntList(self.rki[str(wordID)])


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
                wordID = self.wordHash[word]
                for pageID in self.pageIDsForWordID(wordID):
                    hits[pageID] = hits.get(pageID, 0) + 1
            else:
                # this word wasn't found.
                pass


        # sort results by relevance
        res = hits.keys()
        res.sort(lambda a,b,h=hits: cmp(h[a],h[b]))
        

        # get the labels for the pageIDs
        for i in range(len(res)):
            res[i] = self.getLabel(res[i])

        return tuple(res)



    ## this should go away ##################################################

    def index(self, key, text):
        self.addPage(key, text)
