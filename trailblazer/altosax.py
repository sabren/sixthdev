* saxophone
import atexit, unittest
atexit.register(unittest.main)

** rationale
*** want with small objects / composition
*** PyDispatch gets it right but let's do xml-specific

import xml.sax
    pass


well, okay, I know what the solution should look
like but I don't know what the problem space looks
like. :)

ANYTAG = object()

class SAXophone(xml.sax.ContentHandler):
    def __init__(self):
        self.stack = []
        self.tagMap = {}
    def startDocument(self):
        self.handler = self.getDefaultHandler()
    def getDefaultHandler(self):
        if not self.tagMap.get(ANYTAG):
            raise NotImplementedError("you need to call .byDefault() first")
    def byDefault(self):
        tagMap[ANYTAG] = 
    def startElement(self):
        self.stack.append(self.handler)
        self.handler = getTagHandler(tag, attrs)
    def endElement(self):
        assert self.stack, "stack should never be empty here"
        result = self.handler.onEnd()
        self.handler = self.stack.pop()
        self.handler.onChild(result)
    def characters(self, ch):
        self.handler.onText()
    def whitespace(self, ch):
        self.handler.onWhitespace()


*** byDefault(thunk)
*** onTag(tag, thunk)
*** parse(file)
*** parseString(s)
** tag handlers
*** __init__(attrs)
*** onText()
*** onChild()
*** onWhitespace()
*** onEnd() -> result
** passthrough tag handler
*** collect text, whitespace, child as string
*** just rebuild tag onEnd()

