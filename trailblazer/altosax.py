# altosax:
#
# bootstrap version of saxophone
#
# ugh. this is hard to explain without already
# having trailblazer, so i just wrote a simple
# version, and will write the real saxophone
# once my narrative tools are working.

#*** want with small objects / composition
#*** PyDispatch gets it right but let's do xml-specific

# we'll need this DOCUMENT variable later. It's
# just a fake tag that we use to describe the
# document as a whole. It's just a node that
# contains the root element, just like the
# document node in the W3C DOM.
DOCUMENT = "*top*" 

# okay. so we're going to build our dispatch
# tool as an xml.sax.ContentHandler.
import xml.sax
############################################################
class Saxophone(xml.sax.ContentHandler):
############################################################
    
# We're going to pass all content to a TagHandler,
# so we start up with a default handler:

    def __init__(self, byDefault=None):
        # (first version)
        self.byDefault = byDefault

    def startDocument(self):
        # here's where we use that DOCUMENT tag.
        # pretending its a real tag just simplifies
        # the implementation a bit.
        self.handler = self.getTagHandler(DOCUMENT, {})

# TagHandlers will need .chars() and .space()

    def characters(self, ch):
        self.handler.chars(ch)

    def whitespace(self, sp):
        self.handler.space(sp)

# we want to specify what each tag does, so
# we need a dictionary

    def __init__(self, byDefault=None):
        # (second version)
        self.byDefault = byDefault
        self.tagMap = {}

    def onTag(self, tag, doWhat):
        self.tagMap[tag] = doWhat

# since tags are nested, we need a stack:

    def __init__(self, byDefault=None):
        # (third and final version)
        self.byDefault = byDefault
        self.tagMap = {}
        self.stack = []

    def startElement(self, tag, attrs):
        self.stack.append(self.handler)
        self.handler = self.getTagHandler(tag, attrs)

# by default, our tagMap should just be a
# TagHandler class, or a callable that takes
# the "tag" and "attrs" argument and returns a TagHandler

    def getTagHandler(self, tag, attrs):
        return self.tagMap.get(tag, self.byDefault)(tag, attrs)

# When the tag ends, we need to pass the result to
# the parent tag, so TagHandler needs .close()
# [which returns the result] and .child() [which
# accepts the result from the child]
        
    def endElement(self, tag):
        assert self.stack, "stack should never be empty here"
        result = self.handler.close()
        self.handler = self.stack.pop()
        self.handler.child(result)

# finally, some utility methods because xml.sax is ugly:

    def parse(self, filename_or_stream):
        xml.sax.parse(filename_or_stream, self)
        return self.handler

    def parseString(self, string):
        xml.sax.parseString(string, self)
        return self.handler
        

############################################################
class TagHandler(object):
############################################################
# so here's our base Tag Handler class, with a
# simple default implementation:

    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.data = []

    def chars(self, data):
        self.data.append(data)

    def space(self, data):
        self.data.append(data)

    def child(self, data):
        self.data.append(data)

# what you return at the end is up to you.
# here again is a simple default implementation:

    def close(self):
        return self

# since this class basically builds a dom, it might be
# handy to dump it back to xml:

    def __str__(self):
        res = []

        # open the tag:
        # but not for the virtual DOCUMENT element
        if self.tag != DOCUMENT:
            res.append("<%s" % self.tag)
            # add the attributes
            for key, value in self.attrs.items():
                # note: because attrs is a dict, and
                # dict keys are ordered arbitrarily, this
                # won't match input exactly. :/
                res.append(' %s="%s"' %
                           (key,
                            # also we need to re-encode the data:
                            xmlEncode(value)))
            res.append(">")
       
        # walk the tree recursively:
        for item in self.data:
            res.append(str(item))
            
        # close the tag and squish it all together:
        if self.tag != DOCUMENT:
            res.append("</%s>" % self.tag)
            
        return "".join(res)

# here's that xmlEncode function we called
def xmlEncode(s):
    """
    xmlEncode(s) ->  s with >, <, and & escaped as &gt;, &lt; and &amp;
    """
    ents = {
        ">": "&gt;",
        "<": "&lt;",
        "&": "&amp;"
    }
    return "".join([ents.get(ch,ch) for ch in s])


# okay, we're done. I dind't know how to write this test
# first and incementally. It's kind of a gestalt.
# but, here's how it should work:
import unittest
class SaxophoneTest(unittest.TestCase):
    def test(self):
        s = Saxophone(TagHandler)
        xml = """<data><a>
           here is some <xml version="1.0">xml</xml>
              </a>  
    with some            funky <n>wh
    <n>i
    <foo>tes</foo>
          pa</n>ce</n>
              </data>"""
        self.assertEquals(xml, str(s.parseString(xml)))
        

# If you run this file, it should pass the tests.
if __name__=="__main__":
    unittest.main()
