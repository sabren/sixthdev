
import unittest
import ensemble

class PerlChildTest(unittest.TestCase):

    def setUp(self):
        self.prox = ensemble.Director("perl -w ensemble.pl")
        self.prox.loadModule("PerlChildTest", "perl")

    def test_hello(self):
        self.assertEquals("hello, world!", self.prox.perl.hello())

    def test_add(self):
        self.assertEquals(3, self.prox.perl.add(1, 2))

    def test_fail(self):
        self.assertRaises(ensemble.Fault, self.prox.perl.fail)


if __name__=="__main__":
    unittest.main()
    
