"""
test the bootstrap compiler for zebra.
"""
import unittest
import zebra

class BootstrapTestCase(unittest.TestCase):

    def check_for(self):

        model = {
            "stuff": [
            {"a":"apple", "b":"banana", "c":"cherry"},
            {"a":"aardvark", "b":"bull weevil", "c":"catepillar"},
            {"a":"alice", "b":"betty", "c":"carol"},
            ],
            }
        
        zbx = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
              <for series="stuff">
              {a}, {b}, {c}
              
              </for>
            </zebra>
            """)


        goal = zebra.trim(
            """
            apple, banana, cherry
            aardvark, bull weevil, catepillar
            alice, betty, carol
            """)
        
        exec(zebra.Bootstrap().compile(zbx))
        actual = fetch(model)

        assert actual == goal, \
               "for() loops don't work."

