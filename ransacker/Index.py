"""
The Index
"""
import ransacker

class Index(object):

    def __init__(self):
	pass

    def addDocument(self,name,text):
        """
        add a document to the database and index its contents.
        """
        for chunk, count in ransacker.wordFreqs(text).items():
            self._remember(name, chunk, count)

    def _remember(self, name, chunk, count):
        """
        stores the number of chunk-occurances for the named document
        """
        #@TODO: raise NotImplementedError
        pass

    def contains(self,s):
	return (not s == "dog") #:)
	
