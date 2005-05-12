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
            <rem> ignore me! </rem>
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
            "a":"alaska",
            "stuff":[
                {"a":"apple", "b":"banana", "c":"cherry"},
                {"a":"aardvark", "b":"bull weevil", "c":"catepillar"},
                {"a":"alice", "b":"betty", "c":"carol"},
                ],
            }
        
        zbx = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <rem>test scope</rem>
            <xpr>a</xpr><nl/>
            <for series="stuff">
            <xpr>a</xpr>, <xpr>b</xpr>, <xpr>c</xpr>
            <nl/>
            </for>
            <xpr>a</xpr><nl/>
            </zebra>
            """)

        goal = zebra.trim(
            """
            alaska
            apple, banana, cherry
            aardvark, bull weevil, catepillar
            alice, betty, carol
            alaska
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
            <for series="names">
            <if condition="name=='a'">Argentina</if>
            <ef condition="name=='b'">Bolivia</ef>
            <el>Chile</el>
            <glue>, </glue>
            </for>
            </zebra>
            """)
        goal = "Argentina, Bolivia, Chile"

        
        actual = zebra.Bootstrap().toObject(zbx).fetch(model)
        assert actual== goal, \
               "if/el/ef don't work:\n---%s---" % actual


        
    def check_none(self):
        model = {"emptylist": [],
                 "fulllist": [{"a":"b"}]}
        zbx = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <for series="emptylist">
            THIS SHOULD NOT SHOW UP
            </for>
            <none>
            Nothin's empty. 
            </none>
            <for series="fulllist">
            Somethin's full.
            </for>
            <none>
            THIS SHOULD NOT SHOW UP
            </none>
            </zebra>
            """)

        goal = "Nothin's empty. Somethin's full."

        actual = zebra.Bootstrap().toObject(zbx).fetch(model)
        assert actual == goal, \
               "none doesn't work:\n%s" % actual


    def check_xpr(self):
        zbx = "<zebra><xpr> (1 + 1) * 5 - 8 </xpr></zebra>"
        goal = "2"
        actual = zebra.Bootstrap().toObject(zbx).fetch()
        assert actual == goal, \
               "expressions don't work:\n%s" % actual

    def check_whitespace(self):
        zbx = zebra.trim(
            """
            <zebra>
            <xpr>5</xpr> <xpr>2</xpr><nl/>
            </zebra>
            """)
        goal = "5 2\n"        
        actual = zebra.Bootstrap().toObject(zbx).fetch()
        assert actual == goal, \
               "whitespace is screwed up:\n%s" % actual

    def check_exec(self):
        # note: the <>'s mean something!
        zbx = zebra.trim(
            """
            <zebra>
            <exec>
            ex = '&lt;executive'
            ex = ex + ' decision&gt;'
            </exec>
            <xpr>ex</xpr>
            </zebra>
            """)

        goal = "<executive decision>"
       
        actual = zebra.Bootstrap().toObject(zbx).fetch()
        assert actual == goal, \
               "expressions don't work:\n%s" % actual



    def check_headFootSimple(self):

        # check the simple case, not the grouped version.
        
        model = {
            "list": [
            {"toy":"ball"},
            {"toy":"yoyo"},
            ]}

        zbx = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <for series="list">
            <head>Some toys: [</head>
            <var>toy</var>
            <glue>, </glue>
            <foot>]</foot>
            </for>
            </zebra>
            """)
        
        goal = "Some toys: [ball, yoyo]"

##         print '--------'
##         print zebra.Bootstrap().compile(zbx)
##         print '--------'
        
        actual = zebra.Bootstrap().toObject(zbx).fetch(model)
        assert actual == goal, \
               "head/tails don't work:\n%s" % actual

    def check_nested_for(self):
        model = {"all": [{"subs":[{"value":"a"}]},
                         {"subs":[{"value":"b"}]}]}
        zbx = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <for series="all">
            <head>[</head>
            <for series="subs">
            <head>{</head>
            <var>value</var>
            <foot>}</foot>
            </for>
            <foot>]</foot>
            </for>
            </zebra>
            """)
        goal = "[{a}{b}]"
        actual = zebra.Bootstrap().toObject(zbx).fetch(model)
        self.assertEquals(actual, goal)
        


    def check_include(self):
        zbx = zebra.trim(
            """
            <zebra>
            <include file="test/includefile">
            </include>
            </zebra>
            """)

        goal = "This is the include file!\n"
        actual = zebra.Bootstrap().toObject(zbx).fetch()
        assert actual == goal, \
               "includes don't work:\n%s" % actual

    def check_brackets(self):
        zbx = '<zebra><xpr> ("a","b","c")[1] </xpr></zebra>'
        goal = "b"
        actual = zebra.Bootstrap().toObject(zbx).fetch()
        assert actual == goal, \
               "brackets cause problems:\n%s" % actual
        
    def check_body(self):
        zbx = '<zebra><body>blah</body></zebra>'
        goal = "blah"
        actual = zebra.Bootstrap().toObject(zbx).fetch()
        assert actual == goal, \
               "<body> doesn't work:\n%s" % actual
        
