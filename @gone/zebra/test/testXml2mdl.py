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
        x2m = zebra.xml2mdl.X2mParser()

        assert x2m.model == [], \
               "Doesn't initialize model."

        # now test for the correct model:
        goal = [
            {"__tag__":"top", "__data__" :
             [{"__tag__":"person", "name":"Michal", "__data__":
               [{"__tag__":"skill", "__data__":["Python"]},
                {"__tag__":"skill", "__data__":["ASP"]}]
               }]
             }]
        
        
        x2m.feed(self.data)
        assert x2m.model == goal, \
               "Doesn't build model correctly:\n%s" % x2m.model



