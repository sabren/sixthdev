#!/usr/bin/python
#$Id$
"""
Check for overlapping (duplicate) lines in python files.
Report shows how many lines were in common, and then shows
each line.

The numbers on the left indicate the number of times the
line is duplicated in each file.

Note that this does NOT show lines that are repeated but
only in one file. (We collect that information, but if you
want it, you'll have to write it yourself.)
"""
import os
import os.path

class Overlap:
    """
    I'm an easy-to-sort object representing overlap between files.
    """
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.ms=[]
    def keep(self, string):
        self.ms.append(string)
    def files(self):
        return self.a, self.b
    def matches(self):
        return self.ms
    def __cmp__(self, other):
        return - cmp(len(self.ms), len(other.ms))


class LineIndex:
    """
    I remember where certain strings are found,
    so I can help find duplicate lines and similar files.
    """
    def __init__(self, ignoreParam=None):
        self.data = {}
        self.ignore = ignoreParam or [
            'if __name__=="__main__":',
            '"""',
            'try:',
            'else:',
            'finally:',
            'pass',
            '',
        ]
        
    ## stuff for building the index ########################

    def index(self, dirname):
        os.path.walk(dirname, self._callbackForWalk, arg=None)

    def indexFile(self, dirname, fname):
        path = dirname + os.sep + fname
        for line in open(path):
            if not self.ignorable(line.strip()):
                # s/fname/path/ here if you want precision:
                self.tally(line.strip(), fname) 

    def tally(self, aString, whereFound):
        self.data.setdefault(aString, {})
        self.data[aString].setdefault(whereFound, 0)
        self.data[aString][whereFound] += 1

    def ignorable(self, string):
        return string in self.ignore or string.startswith("import ")

    def _callbackForWalk(self, arg, dirname, fnames):
        for fname in fnames:
            if fname.endswith(".py"):
                self.indexFile(dirname, fname)


    ## reporting  ##########################################

    def getTally(self, aString, whereFound):
        return self.data[aString][whereFound]
                        
    def getOverlaps(self):
        assert self.data != {}, "can't report before indexing!"
        inCommon = {}
        for string, histogram in self.data.items():
            files = histogram.keys()
            for each in files:
                for other in files:
                    if each < other:
                        inCommon.setdefault((each, other), Overlap(each,other))
                        inCommon[(each, other)].keep(string)
        res = inCommon.values(); res.sort()
        return res


if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        dir = sys.argv[1]
    else:
        dir = "."
    idx = LineIndex()
    idx.index(dir)
    for overlap in idx.getOverlaps():
        print "%s and %s have %s line(s) in common:" \
              % (overlap.a, overlap.b, len(overlap.matches()))
        for match in overlap.matches():
            print "%i:%i    %s" % (idx.getTally(match, overlap.a),
                                   idx.getTally(match, overlap.b),
                                   match)
