"""
ransacker: a python search engine
"""
__ver__="$Id$"

from IdMap import *
from Index import Index
from MkIndex import *
from AllMkIndex import *
from SQLiteIndex import *
from vectorspace.search_mod import VectorSpace

NEXTNUM = "\t:nextnum"

## utility functions ####################################

def wordFreqs(text):
    """
    Return a dict mapping words to frequencies
    """
    fd = {}
    for word in text.split():
        if fd.has_key(word):
            fd[word] = fd[word] + 1
        else:
            fd[word] = 1
    return fd


def uniqueWords(text):
    """
    return a list of unique words in a text
    """
    return wordFreqs(text).keys()
