"""
An index that uses MetaKit as the backend.
"""
__ver__="$Id$"

import anydbm
import metakit
import ransacker

class MkIndex(ransacker.Index):

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
        
    def _storeFreq(self, name, word, count):
        self.index.append([self.words[word], self.pages[name], count])

    def score(self, word):
        res = self.index.select(word=self.words[word])
        res = res.sortrev([self.index.count], [self.index.count])
        return tuple([(self.pages[row.page], row.count) for row in res])
    

    def contains(self, name):        
        return self.pages.has_key(name)
