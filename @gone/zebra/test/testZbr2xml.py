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

        ## the blank line before the * checks for a
        ## whitespace error!
        zbr = zebra.trim(
            """
            This is normal text.
            
            * if 1==2:
                This should never show up.
            * el:
            This line isn't part of the else.
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            This is normal text.
            
            <if condition="1==2">
            This should never show up.
            </if>
            <el>
            </el>
            This line isn't part of the else.
            </zebra>
            """)
        
        actual = zebra.zbr2xml.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't indent correctly:\n%s" % actual



    def check_xmlchars(self):
        zbr = zebra.trim(
            """
            <P>Hello&nbsp;World!!! ><
            """)
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            &lt;P&gt;Hello&amp;nbsp;World!!! &gt;&lt;
            </zebra>
            """)

        actual = zebra.zbr2xml.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't cope with xmlchars correctly:\n%s" % actual


    def check_var(self):
        zbr = zebra.trim(
            """
            {
            My name is {?name?}.
            }
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            {
            My name is <var>name</var>.
            }
            </zebra>
            """)
        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't cope well with {?vars?}:\n%s" % actual


    
    def check_expr(self):
        zbr = zebra.trim(
            """
            I will be {:age + 4:} next year.
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            I will be <xpr>age + 4</xpr> next year.
            </zebra>
            """)
        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't cope well with {:exprs:}:\n%s" % actual

    def check_exec(self):
        zbr = zebra.trim(
            """
            * exec:
                name = 'fred'
                xml = '<xml>woohoo!</xml>'
                dict = {}
                dict['a'] = 'b'
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <exec>
            name = 'fred'
            xml = '&lt;xml&gt;woohoo!&lt;/xml&gt;'
            dict = {}
            dict['a'] = 'b'
            </exec>
            </zebra>
            """)
        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't cope well with exec:\n%s" % actual



    def check_invalid(self):
        "check invalid tags"
        zbr = zebra.trim(
            """
            * thisIsAnInvalidTag
            """)
        try:
            zebra.Z2X().translate(zbr)
        except:
            gotError = 1
        else:
            gotError = 0

        assert gotError, \
               "Didn't get error on invalid tag."


    def check_comment(self):
        zbr = zebra.trim(
            """
            *# this is a comment
            this isn't
            *     # this is
            """)
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <rem>this is a comment</rem>
            this isn't
            <rem>this is</rem>
            </zebra>
            """)
        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't handle comments right:\n%s" % actual
            


    def check_include(self):
        #@TODO: drop trailing : from include syntax
        zbr = zebra.trim(
            """
            * include includefile:
            """)

        #@TODO: it should realy be <include file="includefile"/>
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <include file="includefile">
            </include>
            </zebra>
            """)
        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't handle includes right:\n%s" % actual
    


    def check_forNone(self):
        zbr = zebra.trim(
            """
            * for people:
                {?name?} is a nice person.
            * none:
                No people here!
            """)
        
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <for series="people">
            <var>name</var> is a nice person.
            </for>
            <none>
            No people here!
            </none>
            </zebra>
            """)

        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "Doesn't do for..none right:\n%s" % actual


    def check_forHeadBodyFoot(self):
        zbr = zebra.trim(
            """
            * for people:
                * head:
                    PEOPLE
                    -------
                * body:
                    {?name?} is a nice person.
                * foot:
                    -------
                    THE END
            """)
        
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <for series="people">
            <head>
            PEOPLE
            -------
            </head>
            <body>
            <var>name</var> is a nice person.
            </body>
            <foot>
            -------
            THE END
            </foot>
            </for>
            </zebra>
            """)

        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "Doesn't do for/head/body/foot right:\n%s" % actual


    def check_notBlocks(self):
        zbr = zebra.trim(
            """
            * if x==1:
                * include page_one;
            * ef x==2:
                * include page_two;
            """)
        
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <if condition="x==1">
            <include file="page_one"/>
            </if>
            <ef condition="x==2">
            <include file="page_two"/>
            </ef>
            </zebra>
            """)

        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "Doesn't handle ; blocks right:\n%s" % actual

