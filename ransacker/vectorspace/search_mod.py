#!/usr/bin/env python

"""
Cornerhost Searcher Indexer
This should index and search and do all kinds of fun stuff
"""

import sys
try:
    from Numeric import *
except:
    from numpy import *
import re
from string import lower
from stemmer import PorterStemmer
from vecmath import vcos
import ransacker


class VectorSearchEngine(object):
    def __init__(self, index):
        self.index = index
        word_index = self.mapWordsToPosition()
        self.vecs = []
        self.doc_vecs = []
        self.threshold = 0.04
        self.word_index = word_index
        self.build_vectors()

    def build_vectors(self):
        # @TODO: assert 0, "get rid of reliance on self.index.docs"
        # Basically, this class is making its own index.
        # The goal now is to get this to run off of
        # a ransacker.Index instead.
        for doc in self.index.docs:
            vec = self.make_vector(doc)
            # the perl used at this point is
            #   push @vecs, norm $vec;
            # must impliment using Numeric
            self.vecs.append(vec)

        self.doc_vecs.extend(self.vecs)


    def make_vector(self,in_words):
        # words should be a dictionary
        words = get_words(in_words)
        word_count = len(self.word_index.keys())
        vector = zeros(word_count)

        for w in words.keys():
            if self.word_index.has_key(w):
                value = words[w]
                offset = self.word_index.get(w,0) 
                vector[offset] = value
        return vector       

    def search(self,search_for):
        qvec = self.make_vector(search_for)
        result_list = self.get_cosines(qvec)
        documents = {}
        for index in result_list.keys():
            doc = self.index.docs[index]
            relevance = result_list[index]
            documents[doc] = relevance
        return documents

    def get_cosines(self,in_qvec):
        cosines = {}
        index = 0

        for this_vec in self.doc_vecs:
            assert isinstance(this_vec, ArrayType)
            cosine = vcos(this_vec, in_qvec)
            if cosine > self.threshold:
                cosines[index] = cosine
            index = index + 1
        return cosines

    def mapWordsToPosition(self):
        # create a lookup hash of word to position
        # originally looked like this
        # my %lookup;
        # my @sorted_words = sort keys %all_words;
        # @lookup{@sorted_words} = (1..$#sorted_words );    
        lookup = {}
        x = 0
        for one in self.index.getWordList():
            lookup[one] = x
            x = x + 1
        ####  TODO: the above section could(and should) be optimized

        return lookup

class VectorSpace(ransacker.Index):

    def __init__(self, docs):

        self.docs = docs
        self.all_words = {}


    def build_index(self):
        for doc in self.docs:
            self.addDocumentWords(doc)


    def getEngine(self):       
        return VectorSearchEngine(self)



    def addDocumentWords(self, doc):
        words = get_words(doc)            
        for k in words.keys():
            self.all_words.setdefault(k,0)
            self.all_words[k] += words[k]   

    def getWordList(self):
        words = self.all_words.keys()
        words.sort()
        return words


def get_words(text):
    stop_list = load_stop_list() # love those ()
    # Splits on whitespace and strips some punctuation      
    words = [stem(word) for word in text.lower().split()
        if re.match("[a-z\-']+", word)
        and word not in stop_list]
        
    # do { $_++ } for @doc_words{@words};
    doc_words = {}
    for one in words:
        doc_words.setdefault(one,0)
        doc_words[one] = doc_words[one] + 1
            
        # return %doc_words;
    return doc_words

def stem(word):
    # word needs to be all lowercase before being passed to stem
    string.lower(word)  

    # fancy stuff to remove .,?!"
    mymatch = re.compile('(\,|\.|\!|\?|\")')
    word = mymatch.sub(r'',word)

    p = PorterStemmer()
    word = p.stem(word, 0,len(word)-1)
   
    return word


def load_stop_list():
    all_from_file = []
    # @TODO: unhardcode this path. 
    for line in open('./vectorspace/stop_list.txt').readlines():
        mymatch = re.compile('\n')                
        all_from_file.append(mymatch.sub(r'',line))
    
    return all_from_file

        
if __name__=="__main__":
    pass

