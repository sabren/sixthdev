import ransacker

class Index(object):
    """
    This is a fairly wasteful in-memory index.
    Okay for testing, but you almost certainly
    want to use one of its subclasses for any
    real work.

    (Even so, it's 5x faster than MkIndex)

    If you're subclassing this, you want
    to override these methods:

       __init__
       _storeFreq
       _getPageID
       score
       contains
       remove
       
    """

    def __init__(self):
        self.data = {}

    def _getPageID(self, name):
        return name

    def addDocument(self, name, text):
        """
        add a document to the database and index its contents.
        """
        if self.contains(name):
            self.remove(name)
        self._doIndexing(name, text)

    def _doIndexing(self, name, text):
        # fetch pageID only once for speed
        pageID = self._getPageID(name)
        for chunk, count in ransacker.wordFreqs(text).items():
            self._storeFreq(pageID, chunk, count)

    def _storeFreq(self, name, word, count):
        """
        stores the number of word-occurances for the name
        """
        self.data.setdefault(name, {})
        self.data[name][word] = count

    def score(self, word):
        """
        return tuple of (page, count) matches (sort by relevance)
        """
        res = []
        for page in self.data.keys():
            if self.data[page].has_key(word):
                res.append((page, self.data[page][word]))
        
        byRelevance = lambda a,b: -cmp(a[1], b[1])
        res.sort(byRelevance)
        return tuple(res)
        

    def contains(self, name):
	return self.data.has_key(name)

    def remove(self, name):
        del self.data[name]
    
    
    def match(self, word):
        """
        return tuple of pages that match (sort by relevance)
        """
        return tuple([x[0] for x in self.score(word)])
