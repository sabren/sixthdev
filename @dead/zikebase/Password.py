"""
A password class for comparing encrypted passwords

$Id$
"""

class Password:
    """ Example:
    
    >>> pw = Password()
    >>> pw.set('my password')
    >>> pw
    Password('$1$pw$rwL3iXNa3zKvh59Z6jpxc1')
    >>> pw == "my password"
    1
    """

    def __init__(self, crypted=None):
        self.crypted = crypted

    def __repr__(self):
        if self.crypted:
            return "zikebase.Password('%s')" % self.crypted
        else:
            return "zikebase.Password()"

    def __cmp__(self, other):
        if isinstance(other, Password):
            return cmp(self.crypted, other.crypted)
        else:
            return cmp(self.crypted, self.crypt(other))
        
    

    ## public methods ############################
    
    def crypt(self, plain):
        """You can override this to use your favorite one-way encryption"""
        import md5crypt
        return md5crypt.md5crypt(plain, "pw")
    
    def set(self, plain):
        """Set (and encrypt) the password"""
        self.crypted = self.crypt(plain)

