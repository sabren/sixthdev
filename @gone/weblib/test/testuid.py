#
# testuid.py - unit tests for uid.py
#

import unittest
from weblib import uid

class uidTestCase(unittest.TestCase):
    def checkUniqueness(self):
        hash = {}
        howmany = 10000

        print "generating", howmany, "uids..."
        for x in range(howmany):
            id = uid()
            if hash.has_key(id):
                hash[id] = hash[id]+1
            else:
                hash[id] = 1

        print "looking for duplicates..."

        dupefound = 0
        for x in hash.keys():
            if hash[x] > 1:
                print x, hash[x]
                dupefound = dupefound + 1

        # print the results, or throw an error:
        assert not dupefound, "duplicates found. :("
        print "no duplicates! yay!"

