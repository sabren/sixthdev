"""
test the zbr2xml stuff

$Id$
"""
import unittest
import zebra

class Zbr2xmlTestCase(unittest.TestCase):

    def check_simple(self):
        zbr = zebra.trim(
            """
            hello, world!
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            hello, world!
            </zebra>
            """)

        actual = zebra.zbr2xml.Z2X().translate(zbr)
        assert actual==goal, \
               "zbr2xml doesn't translate simplest case:\n%s" % actual
        

        
    def check_indent(self):
        zbr = zebra.trim(
            """
            This is normal text.
            * if 1=2:
                This should never show up.
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            This is normal text.
            <if condition="1=2">
            This should never show up.
            </if>
            </zebra>
            """)
        
        actual = zebra.zbr2xml.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't indent correctly:\n%s" % actual
