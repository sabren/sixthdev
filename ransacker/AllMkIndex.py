"""
An index that uses MetaKit as the backend.

This alternate version also uses Mk for IdMaps...

But don't use it.... It's about 36 times slower. :)
"""
__ver__="$Id$"

import anydbm
import ransacker
try:
    import metakit
except ImportError:
    metakit = None


class MkIdMap:
    def __init__(self, mkdb, name):
        if not metakit:
            raise ImportError("couldn't load metakit")
        
        self.db = mkdb
        self.name = name
        self.view = mkdb.getas("%s[key:S,val:I]" % name)
        
    def __getitem__(self, item):
        if type(item) in (str, unicode):
            # word -> ID
            res = self.view.select(key=item)
            if res:
                return res[0].val
            else:
                #NOTE: this relies on never deleting anything,
                #or you'll get duplicate keys... :)
                ID = len(self.view)+1
                self.view.append([item, ID])
                return ID
        else:
            # ID -> word
            res = self.view.select(val=item)
            if res:
                return res[0].key
            else:
                raise KeyError, "%s not found in map '%s'" % (key,self.name)


class AllMkIndex(ransacker.MkIndex):

    def __init__(self, name=None):
        if name:
            self.db = metakit.storage(name+".rki",1)
        else:
            self.db = metakit.storage()
        self.words = MkIdMap(self.db, "words")
        self.pages = MkIdMap(self.db, "pages")
        self.index = self.db.getas("index[word:I,page:I,count:I]")


if __name__=="__main__":
    mkdb = metakit.storage()
    imap = MkIdMap(mkdb, "map")
    assert imap["cat"] == 1, "first cat broke"
    assert imap["dog"] == 2, "dog broke"
    assert imap["cat"] == 1, "second cat broke: %s" % imap["cat"]
