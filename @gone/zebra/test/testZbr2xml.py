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
            """)

        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <exec>
            name = 'fred'
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
            """)
        goal = zebra.trim(
            """
            <?xml version="1.0"?>
            <zebra>
            <rem> this is a comment</rem>
            this isn't
            </zebra>
            """)
        actual = zebra.Z2X().translate(zbr)
        assert actual==goal, \
               "doesn't handle comments right:\n%s" % actual
            


    def check_for(self):
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
