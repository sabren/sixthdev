__ver__="$Id$"

import unittest
from weblib import Engine
from weblib import OutputDecorator

class OutputDecoratorTest(unittest.TestCase):

    def wrap(self, code):
        eng = Engine(script=code)
        eng.run()
        out = OutputDecorator(eng)
        return out
        
    def test_normal(self):
        out = self.wrap("print >> RES, 'hello, world!'")
        self.assertEquals(out.getHeaders(), 'Content-type: text/html\n\n')
        self.assertEquals(out.getBody(), 'hello, world!\n')

    def test_assert(self):
        out = self.wrap("assert 0, 'the assertion failed'")
        self.assertEquals(out.getHeaders(), 'Content-type: text/html\n\n')
        assert out.getBody().count('the assertion failed'), out.getBody()

    def test_except(self):
        out = self.wrap("raise hell")
        self.assertEquals(out.getHeaders(), 'Content-type: text/html\n\n')
        assert out.getBody().count('NameError'), out.getBody()
        

if __name__=="__main__":
    unittest.main()


