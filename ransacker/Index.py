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
       score
       contains
       remove
       
    """

    def __init__(self):
        self.data = {}

    def addDocument(self, pageName, text):
        """
        add a document to the database and index its contents.
        """
        if self.contains(pageName):
            self.remove(pageName)
        for chunk, count in ransacker.wordFreqs(text).items():
            self._storeFreq(pageName, chunk, count)

    def _storeFreq(self, pageName, word, count):
        """
        stores the number of word-occurances for the pageName
        """
        self.data.setdefault(pageName, {})
        self.data[pageName][word] = count

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
        

    def contains(self, pageName):
	return self.data.has_key(pageName)

    def remove(self, pageName):
        del self.data[pageName]
    
    
    def match(self, word):
        """
        return tuple of pages that match (sort by relevance)
        """
        return tuple([x[0] for x in self.score(word)])
