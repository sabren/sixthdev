"""
An index that uses MetaKit as the backend.
"""
__ver__="$Id$"

import anydbm
import metakit
import ransacker

class MkIndex(object):

    def __init__(self, name=None):
        if name:
            self.db = metakit.storage(name+".rki",1)
            self.db.autocommit()
            self.words = ransacker.IdMap(anydbm.open(name+".rkw", "cf"))
            self.pages = ransacker.IdMap(anydbm.open(name+".rkp", "cf"))
        else:
            self.db = metakit.storage()
            self.words = ransacker.IdMap()
            self.pages = ransacker.IdMap()
        self.index = self.db.getas("index[word:I,page:I,count:I]")        
        
    def add(self, page, text):
        """
        add a page to the database and index its contents.
        """
        for word, count in ransacker.wordFreqs(text).items():
            self.index.append([self.words[word], self.pages[page], count])

    def score(self, word):
        """
        return tuple of (page, count) matches (sort by relevance)
        """
        res = self.index.select(word=self.words[word])
        res = res.sortrev([self.index.count], [self.index.count])
        return tuple([(self.pages[row.page], row.count) for row in res])
    
    def match(self, word):
        """
        return tuple of pages that match (sort by relevance)
        """
        return tuple([x[0] for x in self.score(word)])
