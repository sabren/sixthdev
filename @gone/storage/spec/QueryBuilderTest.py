
from storage import where
import unittest

class QueryBuilderTest(unittest.TestCase):


    def test_simple(self):
        clause = where('a') < 5
        assert str(clause) == "(a < '5')", clause

    def test_complex(self): 
        a = where("a") == 1
        b = where("b") == 2
        #import pdb; pdb.set_trace()
        clause = a | b
        self.assertEquals(str(clause), "((a = '1') OR (b = '2'))")

    def test_like(self):
        clause = where("name").startswith("a")
        self.assertEquals(str(clause), "(name LIKE 'a%')")
        

if __name__=="__main__":
    unittest.main()


