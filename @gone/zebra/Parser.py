"""
Parses Zebra's XML syntax.

$Id$
"""
import xmllib, os, string

class Parser (xmllib.XMLParser):
    """zebra.Parser - extends xmllib.XMLParser

    The whole point of this parser is to read in the zebra template
    and create a data structure that can be passed to a code
    generator. The data structure looks like this:

        {'stripe' : self.stripe,      # a list of lists
         'named' : self.named,        # a dict of named stripes
         'skins' : self.skins,        # a dict of stripes
         'queries' : self.queries,    # a dict of queries
         'sources' : self.sources}    # a dict of data source definitions

    xmllib.XMLParser is an event-based parser, so in order
    to keep track of where we are, we maintain stacks. See
    reset() for details.

    Some of zebra's structures (reports, skins, etc) are made
    of several pieces... These are stored collectively in
    a dictionaries of various shapes. The current one should
    always be made available through self.struct.

    Likewise, the current stripe - a block of data between xml tags -
    should always be made available via self.stripe.

    At some point, it's very likely that much of this scheme will be
    replaced by a DOM implementation so that more complex
    transformations/etc can happen. These will mostly all be done by
    the parser, and the current returned dict should remain intact
    [though possibly extended] so as not to disturb the various
    Generator subclasses.
    
    """

    ###############################################

    def __init__(self):
        xmllib.XMLParser.__init__(self)

    def reset(self):
        """Resets internal variables.
        called by XMLParser.__init__ and ZebraParser.parse"""

        xmllib.XMLParser.reset(self) # initiate base class

        # there's a .stack internal to XMLParser, but it's semi-protected,
        # and it changed from python 1.5.1 to 1.5.2 ... so I'm implementing
        # my own.. Start with None because "zebra" tag has no parent
        self.tagstack = [None]

        # datstack is a stack of various thingies (stripes/structures)
        self.datstack = []
        # wrapstack keeps track of nested wraps
        self.wrapstack = []

        # these keep track of <site>s
        self.dirstack = [os.getcwd()]
        self.hrefstack = []
        self.crumbstack = []

        # contextstack keeps track of the current context
        #@TODO: context only works with "eval" right now.
        #it should work with show and exec as well..
        self.contextstack = []

        self.named   = {} # named stripes go in here
        self.skins   = {} # skins go in here
        self.queries = {} # queries go in here
        self.sources = {} # sources go in here

        self.struct  = {} # current structure (report, skin, etc)
        self.stripe  = [] # current stripe
        self.parsed  = {} # parsed content
        self.context = "show" # current context
        self.eval    = "" # python code to evaluate

    ###############################################

    def popStruct(self):
        """pops a struct off the datstack"""
        self.struct = self.datstack[-1]
        self.datstack = self.datstack[:-1]

    def pushStruct(self):
        self.datstack.append(self.struct)

    def pushStripe(self):
        self.datstack.append(self.stripe)

    def popStripe(self):
        """Pops a stripe/data off the datstack.."""
        self.stripe = self.datstack[-1]
        self.datstack = self.datstack[:-1]

    ###############################################
        
    def handle_data(self, data):
        """this method adds text to the current stripe,
        unless we're in eval context. Then it adds it to 'eval'.."""


        ## we strip the last newline, so that:
        
        ## * show
        ## abcedefg
        ## * show
        ## hijklmnop

        ## becomes 'abcdefghijklmnop'
        ##
        ## get the newline back just by adding another one.

        if data[-1] == "\n":
            data = data[:-1]

        if self.context == "eval":
            self.eval = self.eval + data
        elif not string.strip(data):
            return
        elif (len(self.stripe) == 0) \
        or (type(self.stripe[-1])!=types.StringType):
            ## time to add a new string to the list
            self.stripe.append(data)
        else:
            ## rather than append, just merge it
            ## with the existing string.
            self.stripe[-1] = self.stripe[-1] + data


    ###############################################

    def start_site(self, attrs):

        # dir is required, but href is optional
        if attrs.has_key("href"):
            pass
        else:
            attrs["href"] = attrs["outdir"]

        # put these things on a stack..
        self.dirstack.append(attrs["outdir"])
        self.crumbstack.append(attrs["crumb"])
        self.hrefstack.append(attrs["href"])

        # how's this for horribly inefficient?
        for d in self.dirstack:
            os.chdir(d)

    def end_site(self):
        self.crumbstack = self.crumbstack[:-1]
        self.hrefstack = self.hrefstack[:-1]
        self.dirstack = self.dirstack[:-1]
        for d in self.dirstack:
            os.chdir(d)

    ###############################################

    def start_page(self, attrs):
        pagetext = open(self.dirstack[0] + "/" + attrs["src"]).read()
        newZebra = Engine().compile(pagetext)
        outfile = open(attrs["out"],"w")
        outfile.write(newZebra)

    def end_page(self):
        pass

    ###############################################

    def start_eval(self, attrs):
        self.contextstack.append(self.context)
        self.context = "eval"
        self.eval = ""

    def end_eval(self):
        self.context = self.contextstack[-1]
        self.contextstack = self.contextstack[:-1]
        exec(self.eval)

    ###############################################

    def start_source(self, attrs):
        self.pushStruct()
        self.pushStripe()
        
        self.struct = {
            "class": attrs["class"] }        
        self.sources[attrs["name"]] = self.struct

        self.stripe = []
        self.struct["connector"] = self.stripe

    def end_source(self):
        self.popStripe()
        self.popStruct()
    
    ###############################################

    def start_query(self, attrs):
        self.pushStruct()
        self.pushStripe()

        self.struct = {
            "source" : attrs["source"] }
        self.queries[attrs["name"]] = self.struct

        self.stripe = []
        self.struct["query"] = self.stripe

    def end_query(self):
        self.popStripe()
        self.popStruct()
    
    ###############################################

    def start_report(self, attrs):
        self.pushStruct()
        self.struct = {
            "tag"   : "report", # call flatten_report() instead of flatten()
            "query" : attrs["query"], # the name of a query 
            "head"  : [],
            "body"  : [],
            "foot"  : [],
            "none"  : [],
            "grouph": [], # group heads
            "groupf": [], # group feet
            "groups": [], # groups (fields)
            "gdepth": 0}  # group depth

    def end_report(self):
        ## append the structure to the current stripe
        self.stripe.append(self.struct)
        self.popStruct()

    ###############################################

    def unknown_starttag(self, tag, attrs):

        tag = string.replace (tag, "z:", "")
        self.tagstack.append(tag)

        if tag == "zebra":
            ## @TODO: handle language attribute.. (do i need one?)
            pass
        elif tag in ["query", "head", "body", "foot", "none"]:
            ## then start a new stripe!
            self.datstack.append(self.stripe)
            self.stripe = []
            ## @TODO: fix this, but figure out what's wrong with it first. :)
            if tag=="query":
                self.struct["source"]=attrs["source"]
        elif tag in ["stripe", "show", "exec", "if", "el", "ef"]:
            ## these are all special stripes with predefined properties
            if tag=="stripe" and attrs.has_key("name"):
                ## start a new stripe stored in the "named" hash
                self.datstack.append(self.stripe)
                self.stripe = []
                self.named[attrs["name"]] = self.stripe
            else:
                ## @TODO: there ought to be a stack for context..
                ## @TODO: maybe these should be handled seperately?
                ## @TODO: maybe this should all be generic code,
                ## and only fiddled with in compile().. :)
                newStripe = {
                    "tag"         : "stripe",
                    "content"     : [],
                    "context"     : "show",
                    "conditional" : "do",
                    "test"        : ""}
                ## each type of stripe has defaults:
                if tag == "exec" : newStripe["context"] = "exec"
                if tag in ["if", "el", "ef"] : newStripe["conditional"] = tag
                ## stripes let you override those things..
                for key in newStripe.keys():
                    if attrs.has_key(key):
                        newStripe[key] = attrs[key]
                self.stripe.append(newStripe)
                self.datstack.append(self.stripe)
                self.stripe = newStripe["content"]
        elif tag in ["title", "keywords", "description", "content"]:
            ## these are just "named" stripes with predefined names
            self.datstack.append(self.stripe)
            self.stripe = []
            self.named[tag] = self.stripe
        elif tag == "wrap":
            self.wrapstack.append(attrs["skin"])
            self.stripe.append(self.skins[attrs["skin"]]["head"])
        elif tag == "group":
            self.struct["gdepth"] = self.struct["gdepth"] + 1
            self.struct["groups"].append(attrs["field"])
        elif tag == "skin":
            # initialize a new, empty skin:
            self.datstack.append(self.struct)
            self.struct = {"head": "",  "foot": ""}
            self.skins[attrs["name"]] = self.struct
        elif tag == "include":
            incfile = attrs["file"]
            inctext = open(incfile,"r").read()
            newZebra = Engine().parse(inctext)
            self.stripe.append(newZebra["stripe"])
            ## overwrite existing names...???!?!
            ## @TODO: maybe some notion of namespaces?
            for i in newZebra["named"].keys():
                self.named[i] = newZebra["named"][i]
            for i in newZebra["skins"].keys():
                self.skins[i] = newZebra["skins"][i]
        elif tag == "insert":
            self.stripe.append("{!" + attrs["stripe"] + "}")
        else:
            pass # ignore unknown tags


    ###############################################

    def unknown_endtag(self, tag):

        tag = string.replace (tag, "z:", "")
        self.tagstack = self.tagstack[:-1]
        parent = self.tagstack[-1]

        if tag in ["query", "head", "foot", "body", "none"]:
            if parent == "group" and tag in ["head", "foot"]:
                ## grouph will look like: [outer, middle, inner]
                ## groupf will look like: [inner, middle, outer]
                ## It's just easier that way.
                self.struct["group" + tag[0]].append( self.stripe )
            else:
                self.struct[tag] = self.stripe
            self.stripe = self.datstack[-1]
            self.datstack = self.datstack[:-1]
        elif tag in ["skin"]:
            ## just pop the old struct off the stack.
            self.struct = self.datstack[-1]
            self.datstack = self.datstack[:-1]
        elif tag in ["stripe", "description", "content", "keywords", \
                     "title", "show", "exec", "if", "el", "ef"]:
            ## all we have to do is shift our attention to the
            ## parent.. the current stripe is already a part of
            ## the parent..
            self.stripe = self.datstack[-1]
            self.datstack = self.datstack[:-1]
        elif tag == "wrap":
            self.stripe.append(self.skins[self.wrapstack[-1]]["foot"])
            self.wrapstack = self.wrapstack[:-1]
        elif tag == "group":
            ## not all groups have heads or feet If this one
            ## doesn't, even out the stack(s) with an empty value
            if len(self.struct["grouph"]) < len(self.struct["groups"]):
                self.struct["grouph"].append(None)
            ## Remember, groupf is in backwards order from
            ## grouph. It sounds strange, but that actually is what I want,
            ## because that's the order in which I'll need them.
            ## so, grouph and groupf get processed the same here.
            if len(self.struct["groupf"]) < len(self.struct["groups"]):
                self.struct["groupf"].append(None)
        else:
            pass # </zebra>, or unknown tag


    ###############################################

    def parse(self, zbr):

        # if it's not XML-ish, assume it's an outline
        if zbr[0:2] != "<?":
            import o2x
            zbr = o2x.o2x(zbr)

        self.reset()
        self.feed(zbr)
        self.close
        self.parsed = {
            "stripe" : self.stripe,
            "named"  : self.named,
            "skins"  : self.skins,
            "queries": self.queries,
            "sources": self.sources}
        return self.parsed


