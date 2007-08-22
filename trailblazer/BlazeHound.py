"""
This is BlazeHound, our XML-based solution compiler.

Use this if you want to build the entire solution up
through the narrative with all the code embedded
directly in the xml.

If your code is in a source file with tags embedded
in the comments, you want to use LineHound.

Here's what we're shooting for: We should be able
to put a bunch of ideas in the same file and have it
all mixed up, and modify things as we go along so
that we're able to explain things in nice little
pieces... But then in the end we want the computer
to be able to go back and compile all the trails into
the full solution, dumping the tests to one place,
the final code to another, and the docs somewhere else.
so basically we want to parse an xml file and build
a Solution objects
"""

import unittest
class BlazeHoundTest(unittest.TestCase):
    def test(self):
        hound = BlazeHound()
        sol = hound.parseString(
        '''\
        <xml>
          <trail:blaze trail="char">
            <trail:blaze trail="alpha">XYZ</trail:blaze>
            <trail:blaze trail="number">123</trail:blaze>
          </trail:blaze>
          <trail:extend trail="char.number">456</trail:extend>
          <trail:replace trail="char.alpha">ABC</trail:replace>
          <trail:extend trail="char.alpha">DEF</trail:extend>
        </xml>\
        ''')
        logging.debug(sol.getBlazes())
        logging.debug(list(sol))

        # so the alpha and number areas should be easy:
        self.assertEquals("ABCDEF", str(sol["char.alpha"]))
        self.assertEquals("123456", str(sol["char.number"]))

        # and if we clear out the whitespace:
        self.assertEquals("ABCDEF123456",
                          "".join(str(sol["char"]).split()))



"""
So the idea is pretty straightforward. We're just going
to parse the XML file and add all the chunks
to a Solution. So in terms of our technology,
we want to create a Saxophone with some TagHandlers
that build a Solution object from the xml tags.
"""
from Solution import Solution

"""
Since state machines are kind of tricky, we can
use the logging module to help us see what's
happening.
"""
import logging

"""
To see the log output, just uncomment this next line:
"""
#logging.root.setLevel(logging.DEBUG)


"""
So... Our XML format has three tags. We're
going to skirt around the whole issue of xml
namespaces here, because by default, xml.sax
just ignores the colon and returns the whole
qualified name as a string. This means "trail:"
isn't a real xml namespace. That should probably
be fixed later.
"""

#@TODO: clean up namespace handling
TAG_BLAZE = "trail:blaze"
TAG_EXTEND = "trail:extend"
TAG_REPLACE = "trail:replace"

"""
The basic TagHandler class almost does what we
want, but not quite. Why? Because it's appending
to a list as we go along, but what we really want
to do is append to a Solution.

ah, but which Solution? if all we had were blaze
tags, then we could just make up a new Solution
at the start of each tag and build up the tree
using anonymous instances.

But: since we want to be able to modify the tree
as we go (using the replace and extend tags)
then we need to be able to walk the tree at any
time. which means we need to keep a reference
to the root Solution in a variable somewhere.

it also means that we can't have an anonymous
Solution for each tag, which would have been
easier. We need to add each child Solution to
its parent immediately when we start the
trail:blaze tag.

Also, if we want nested blaze tags, then we
need the concept of a "current" solution as
well as the "root" solution. so we need exactly
one root Solution, plus a stack, containing one
Solution per trail tag. (We use a stack because
the tags can be nested). Finally, we need to
keep track of which one is the current solution.

So:
"""
import xml.sax
class BlazeHound(xml.sax.ContentHandler):
    def __init__(self, root=None):
        xml.sax.ContentHandler.__init__(self)
        self.root = root or Solution()     # root Solution 
        self.stack = []            # child Solutions
        self.current = self.root   # current Solution


    """
    Now, the way sax works, there are certain methods that
    get called as you parse from the top of the xml file
    to the bottom, one for each xml concept that you
    encounter.

    So character data, whitespace, and xml entities are
    pretty easy. We just pass the data directly to the
    current Solution:
    """

    # sax content events:
    
    def characters(self, content):
        self.current.append(content)

    def ignorableWhitespace(self, whitespace):
        self.current.append(whitespace)

    def skippedEntity(self, name):
        # handle entities like &amp;
        self.current.append("&%s;" % name)


    """
    Most of the tags should also just pass through
    unchanged to the Solution, but we need to set
    up some special handlers for the three tags
    that we defined earlier.

    So, we'll just hard code some dispatch logic
    for these, and fill them in later:
    """

    def startElement(self, name, attrs):
        method = {
            TAG_BLAZE   : self.tag_blaze,
            TAG_EXTEND  : self.tag_extend,
            TAG_REPLACE : self.tag_replace,
        }.get(name)
        if method:
            method(attrs)
        else:
            self.tag_normal(name, attrs)

    """
    All these special tag handlers are going to push
    the current solution onto the stack, and then pick
    a new solution to be the current one.
    
    After we close a special tag, we just go back to
    working with the previous Solution. All three 
    special end tags will do the same thing, so we
    can just take care of all of them at once:
    """

    def endElement(self, name):
        method = {
            TAG_BLAZE   : self.end_special,
            TAG_REPLACE : self.end_special,
            TAG_EXTEND  : self.end_special,
        }.get(name)
        if method:
            method()
        else:
            self.end_normal(name)

    def end_special(self):
        self.current = self.stack.pop()


    """
    Normal tags just pass through directly. We won't
    always get the exact same start tags since the
    attributes are turned into python dicts, which 
    are unordered. Similarly, <empty/> tags will be
    turned into <empty></empty> tag pairs, but it
    doesn't matter: the xml is equivalent.
    """

    def tag_normal(self, name, attrs):
        self.current.append("<%s" % name)
        for k,v in attrs.items():
            self.current.append(' %s="%s"' % (k, v))
        self.current.append(">")

    def end_normal(self, name):
        self.current.append("</%s>" % name)


    """    
    Now we can consider the special tags individually.
    
    The blaze tag starts a new Solution, so we need
    to push the current solution onto the stack
    and create a new one:
    """

    def tag_blaze(self, attrs):
        trail = attrs["trail"]
        # create the new child solution:
        self.current.blaze(trail)
        # push this one onto the stack
        self.stack.append(self.current)
        # and replace it with the new child
        self.current = self.current[trail]


    """
    The extend tag jumps back to an existing solution:
    """
   
    def tag_extend(self, attrs):
        trail = attrs["trail"]
        # push this one onto the stack
        self.stack.append(self.current)
        # and replace it with the trail
        # by following the dots from the root:
        self.current = self.root[trail]


    """
    And the replace tag does the exact same thing, but
    it clears the previous solution first. Since the
    """

    def tag_replace(self, attrs):
        self.root[attrs["trail"]].clear()
        self.tag_extend(attrs)


    """
    And... That's really all we need.

    Here are two convenience methods though:
    """
    def parse(self, filename_or_stream):
        xml.sax.parse(filename_or_stream, self)
        return self.root

    def parseString(self, string):
        xml.sax.parseString(string, self)
        return self.root
    

# run the tests
if __name__=="__main__":
    unittest.main()
    
