
import unittest
import ensemble

def hello():
    return "hello, world!"

def add(a, b):
    return a + b

def fail():
    raise Exception


class PythonChildTest(unittest.TestCase):

    def setUp(self):
        self.prox = ensemble.Director("python ensemble.py")
        self.prox.loadModule("PythonChildTest", "py")

    def test_hello(self):
        self.assertEquals("hello, world!", self.prox.py.hello())

    def test_add(self):
        self.assertEquals(3, self.prox.py.add(1, 2))

    def test_fail(self):
        self.assertRaises(ensemble.Fault, self.prox.py.fail)


if __name__=="__main__":
    unittest.main()
    
