"""
Test cases for the Rot13Password class

$Id$
"""

import unittest
import zikebase

class Rot13PasswordTestCase(unittest.TestCase):


    def check_rot13(self):
        pw = "~miChaL5zIke90!"
        rot13 = zikebase.Rot13Password()
        rot13.set(pw)
        assert rot13.crypted == "~zvPunY0mVxr45!" , \
               "wrong rot13: %s" % rot13.crypted

        assert rot13.decrypt() == pw, \
               "wrong rot13 decryption."
        
        
        
        
