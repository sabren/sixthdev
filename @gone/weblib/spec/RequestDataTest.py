
import unittest
from weblib import RequestData

class RequestDataTest(unittest.TestCase):

    def test_basics(self):
        s = "a=1&b=2&b=3&e=em+cee+squared"
        q = RequestData(s)
        assert q.string == s
        assert q["a"] == "1", \
               "simple querystring not working"
        assert q["b"] == ("2", "3"), \
               "doesn't tupleize multiple values"
        assert q["e"] == "em cee squared", \
               "query's urldecoding not working"
    
