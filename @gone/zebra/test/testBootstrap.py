"""
test the bootstrap compiler for zebra.
"""
import unittest
import zebra

class BootstrapTestCase(unittest.TestCase):

    def check_basics(self):
        zbx = zebra.trim(
            """
            <zebra>
            hello, world!
            </zebra>
            """)

        rpt = zebra.Bootstrap().toObject(zbx)

        for item in ("fetch", "show"):
            assert hasattr(rpt, item), \
               "Report objects don't have .%s()!" % item

        actual = rpt.fetch()
        assert actual == "hello, world!", \
               "basic 'hello, world' doesn't work:\n%s" % actual

        assert actual == rpt.fetch(), \
               "calling fetch() a second time yields different results. :/"


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
            <var>a</var>, <var>b</var>, <var>c</var>
            <br/>            
            </for>
            </zebra>
            """)

        goal = zebra.trim(
            """
            apple, banana, cherry
            aardvark, bull weevil, catepillar
            alice, betty, carol
            """)
        

        actual = zebra.Bootstrap().toObject(zbx).fetch(model)
        assert actual == goal, \
               "for() loops don't work:\n---\n%s---" % actual


    def check_conditionals(self):
        model = {
            "names": [
            {"name":"a"},
            {"name":"b"},
            {"name":"c"}]
            }
        
        zbx = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <for series="names" glue=", ">
            <if condition="name=='a'">Argentina</if>
            <ef condition="name=='b'">Bolivia</ef>
            <el>Chile</el>
            </for>
            </zebra>
            """)
        
        goal = "Argentina, Bolivia, Chile"

        #print '--------'
        #print zebra.Bootstrap().compile(zbx)
        #print '--------'
        
        actual = zebra.Bootstrap().toObject(zbx).fetch(model)
        assert actual== goal, \
               "if/el/ef don't work:\n---%s---" % actual

