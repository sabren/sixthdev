
from Index import *
from WordHash import *

NEXTNUM = "\t:nextnum"


## utility functions ####################################


def intListToStr(intList):
    import array
    return array.array("I", intList).tostring()

def strToIntList(str):
    import array
    return array.array("I", str).tolist()


def wordFreqs(text):
    """Return a dict mapping words to frequencies"""
    fd = {}
    for word in string.split(text):
        if fd.has_key(word):
            fd[word] = fd[word] + 1
        else:
            fd[word] = 1
    return fd



def uniqueWords(text):
    """return a list of unique words in a text"""
    return wordFreqs(text).keys()
