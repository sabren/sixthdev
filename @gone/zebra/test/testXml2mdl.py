"""
test the xml2mdl routine

$Id$
"""
import unittest
import zebra

class Xml2mdlTestCase(unittest.TestCase):

    def setUp(self):
        self.data = zebra.trim(
            """
            <?xml version="1.0"?>
            <top>
              <person name="Michal">
              <skill>Python</skill>
              <skill>ASP</skill>
              </person>
            </top>
            """)

    def check_X2mParser(self):
        x2m = zebra.xml2mdl.X2M()

        assert x2m.model == [], \
               "Doesn't initialize model."
        
        # now test for the correct model:
        goal = ['\n',
                {'__tag__': 'top',
                 '__data__':
                 ['\n  ',
                  {'__tag__': 'person',
                   '__data__':
                   ['\n  ',
                    {'__tag__':
                     'skill', '__data__':
                     ['Python']},
                    '\n  ',
                    {'__tag__': 'skill',
                     '__data__': ['ASP']},
                    '\n  '],
                   'name': 'Michal'},
                  '\n']},
                '\n']
        
        actual = x2m.translate(self.data)
        assert actual == goal, \
               "Doesn't build model correctly:\n%s" % actual
        
