
from pytypes import EmailAddress
import unittest 

def email(s):
    try:
        return EmailAddress(s)
    except TypeError:
        return 0

class EmailAddressTest(unittest.TestCase):
  
    def testIt(self):
        assert email('sabren@manifestation.com')
        assert email('michal.sabren@manifest-station.com')
        assert not email('laskdjf..asdf@sadf.com')
        assert not email('asdf@@asdf.asc')
        assert not email('aslkdjf')
        
if __name__=="__main__":
    unittest.main()
