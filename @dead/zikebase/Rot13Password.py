"""
A password class with with VERY weak "encryption"

$Id$
"""
import zikebase
zikebase.load("Password")

class Rot13Password(zikebase.Password):
    """
    Use this if you want to EASILY decrypt someone's password
    (perhaps to send people their plaintext password via email)..

    examples:
    >>> import zikebase
    >>> pw = zikebase.Rot13Password()
    >>> pw.set('my password')
    >>> pw.crytped
    zikebase.Rot13Password('zl cnffjbeq')

    >>> zikebase.Rot13Password().crypt('zl cnffjbeq')
    'my password'
    """

    def __repr__(self):
        if self.crypted:
            return "zikebase.Rot13Password('%s')" % self.crypted
        else:
            return "zikebase.Rot13Password()"


    ## public methods ############################
    
    def crypt(self, plain):
        """Doesn't really encrypt, but rotates 13 chars through the alphabet"""


        lowerA = "abcdefghijklmnopqrstuvwxyz"
        lowerB = "nopqrstuvwxyzabcdefghijklm"

        upperA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        upperB = "NOPQRSTUVWXYZABCDEFGHIJKLM"
        
        digitA = "0123456789"
        digitB = "5678901234"


        res = ""
        import string
        for char in plain:
            if char in lowerA:
                res = res + lowerB[string.index(lowerA, char)]
            elif char in upperA:
                res = res + upperB[string.index(upperA, char)]
            elif char in digitA:
                res = res + digitB[string.index(digitA, char)]
            else:
                res = res + char
        return res
            
          
    def decrypt(self):
        """Since rot13 both crypts and decrypts, this just calls .crypt()"""
        return self.crypt(self.crypted)
