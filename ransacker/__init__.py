"""
ransacker: a python search engine

$Id$
"""

from IdMap import *
from MkIndex import *
from AllMkIndex import *

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
