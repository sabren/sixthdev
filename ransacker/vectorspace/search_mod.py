#!/usr/bin/env python

"""
Cornerhost Searcher Indexer
This should index and search and do all kinds of fun stuff
"""

import sys
from Numeric import *
import re
from string import lower
from stemmer import PorterStemmer
from vecmath import vcos

class VectorSpace:

	def __init__(self, docs, stoplist):

		self.word_index = {}
		self.word_count = 0
		self.vecs = []
		self.doc_vecs = []
		self.threshold = 0.04
		self.docs = docs
		self.stop_list = stoplist
		self.all_words = {}


	def build_index(self):
		for doc in self.docs:
		# for doc in self.docs:
                    self.addDocumentWords(doc)
                self.mapWordsToPosition()


        def build_vectors(self):
                assert self.word_count > 0, "must call build_index() first!!"
		for filename in self.docs:
			vec = self.make_vector(filename)
			# the perl used at this point is
			#   push @vecs, norm $vec;
			# must impliment using Numeric
			self.vecs.append(vec)

		self.doc_vecs.extend(self.vecs)



	def search(self,search_for):
		
		qvec = self.make_vector(search_for)
		# print "\nqvec says  ", qvec

		# result_list is a dictionary
		# FIX-ME
		result_list = self.get_cosines(qvec)
		# print "\nresult_list  ", result_list
		
		documents = {}

		for index in result_list.keys():
			doc = self.docs[index]
			relevance = result_list[index]
			documents[doc] = relevance

		return documents

	def get_words(self,text):
		# Splits on whitespace and strips some punctuation		
		# my ( $self, $text ) = @_;
		# my %doc_words;  
		# my @words = map { stem($_) }
		#			grep { !( exists $self->{'stop_list'}->{$_} ) }
		#			map { lc($_) } 
		#			map {  $_ =~/([a-z\-']+)/i} 
		#			split /\s+/, $text;
		doc_words = {}
		words = [self.stem(word) for word in text.lower().split()
			    if re.match("[a-z\-']+", word)
			    and word not in self.stop_list]
		
		# do { $_++ } for @doc_words{@words};
		for one in words:
			doc_words.setdefault(one,0)
			doc_words[one] = doc_words[one] + 1
			
		# return %doc_words;
		return doc_words

	def stem(self, word):
		# word needs to be all lowercase before being passed to stem
		string.lower(word)	

		# fancy stuff to remove .,?!"
		mymatch = re.compile('(\,|\.|\!|\?|\")')
		word = mymatch.sub(r'',word)

		p = PorterStemmer()
		word = p.stem(word, 0,len(word)-1)
		return word


        def addDocumentWords(self, doc):
            words = self.get_words(doc)            
            for k in words.keys():
	        self.all_words.setdefault(k,0)
		self.all_words[k] += words[k]	

        def mapWordsToPosition(self):
		# create a lookup hash of word to position
		# originally looked like this
		# my %lookup;
		# my @sorted_words = sort keys %all_words;
		# @lookup{@sorted_words} = (1..$#sorted_words );	
		lookup = {}
		sorted_words = self.all_words.keys()
		sorted_words.sort()
		x = 0
		for one in sorted_words:
			lookup[one] = x
			x = x + 1
		####  TODO: the above section could(and should) be optimized

                self.word_index = lookup
                self.word_list = sorted_words
                self.word_count = len(sorted_words)


	def make_vector(self,in_words):
		# words should be a dictionary
		words = self.get_words(in_words)
		# the perl used at this point is
		#  my $vector = zeroes $self->{'word_count'}; 
		vector = zeros(self.word_count)
                #assert self.word_count > 0
                #assert type(vector)==array, vector
		# print "\nthe first vector ", vector
		
		# print "\nthe keys are ", words.keys()
		for w in words.keys():
			if self.word_index.has_key(w):
				# print "\nw is ", w
				# print "\nword_index says  ", word_index
				value = words[w]
				# print "\nvalue is", value
				offset = self.word_index.get(w,0) # <-- turns moose into cats
				# print "\noffset is ", offset
				# print "\nvector says ", vector
				vector[offset] = value
				# print "\nvector now says ", vector
                #assert type(vector)==array
		return vector		


	def get_cosines(self,in_qvec):
	
		cosines = {}
		index = 0

		for this_vec in self.doc_vecs:
                        assert isinstance(this_vec, ArrayType)
			cosine = vcos(this_vec, in_qvec)
			# print "\nnew cosine  ", cosine
			if cosine > self.threshold:
				cosines[index] = cosine

			index = index + 1

		return cosines


def load_stop_list():
	all_from_file = []
	for line in open('stop_list.txt').readlines():
		mymatch = re.compile('\n')                
		all_from_file.append(mymatch.sub(r'',line))
	
	return all_from_file


		
if __name__=="__main__":
    
    docs = ["dog", "cat", "dog? cat", "cat cat"]
    engine = VectorSpace(docs, load_stop_list())
    engine.build_index()
    assert engine.word_count > 0
    engine.build_vectors()


    results = engine.search("dog")
    assert results.has_key("dog")
    assert results.has_key("dog? cat")
    assert len(results.keys()) == 2
    assert results["dog"] > results["dog? cat"]

    print "it works!"

		
