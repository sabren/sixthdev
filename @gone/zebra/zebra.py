###################################################
# zebra.py
#
#    python implementation of zebra,
#    an XML-based template engine and code
#       generator
#
#   This code is free and may be redistributed
#   or copied under the terms of the GNU General
#   Public License. See http://www.fsf.org/ for details
#
###################################################
##[ configuration ]################################
###################################################

#@TODO: python 1.5.2 has a new version of xmllib
import xmllib, re, string, types, sys, os

## useMessy allows us to write ill-formed XML so we don't
## have to litter our html with &lt; and &gt; entities
## pretty much superceded by o2x, but what the hey?
## @TODO: this should be part of the engine
useMessy = 0


###################################################
##[ zebra.Engine ]#################################
###################################################

class Engine:
    def __init__(self, generator=None):
        self.parser = Parser()
        if generator == None:
            self.generator = Generator()
        else:
            self.generator = generator
    def compile(self, text):
        return self.generator.generate(self.parser.parse(text))



###################################################
##[ zebra.Parser ]#################################
###################################################

class Parser (xmllib.XMLParser):

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

        self.named  = {} # named structures go in here
        self.skins  = {} # skins go in here

        self.struct  = {} # current structure (report, skin, etc)
        self.stripe  = [] # current stripe
        self.parsed  = {} # parsed content
        self.context = "show" # current context
        self.eval    = "" # python code to evaluate

    ###############################################

    def handle_data(self, data):

        """this method adds text to the current stripe,
        unless we're in eval context. Then it adds it to 'eval'.."""

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

    def unknown_starttag(self, tag, attrs):

        tag = string.replace (tag, "z:", "")
        self.tagstack.append(tag)

        if tag == "zebra":
            ## @TODO: handle language attribute..
            pass
        elif tag == "report":
            self.datstack.append(self.struct)
            self.struct = {
                "tag"  : tag,
                "query": [],
                "head" : [],
                "body" : [],
                "foot" : [],
                "none" : [],
                "grouph": [], # group heads
                "groupf": [], # group feet
                "groups": [], # groups (fields)
                "gdepth": 0}  # group depth
        elif tag in ["query", "head", "body", "foot", "none"]:
            ## then start a new stripe!
            self.datstack.append(self.stripe)
            self.stripe = []
            ## @TODO: fix this:
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
            pass # <zebra>, or unknown tag


    ###############################################

    def unknown_endtag(self, tag):

        tag = string.replace (tag, "z:", "")
        self.tagstack = self.tagstack[:-1]
        parent = self.tagstack[-1]

        if tag in ["query", "head", "foot", "body", "none"]:
            if parent == "group" and tag in ["head", "foot"]:
                ## grouph will look like: [outer, middle, inner]
                ## groupt will look like: [inner, middle, outer]
                ## It's just easier that way.
                self.struct["group" + tag[0]].append( self.stripe )
            else:
                self.struct[tag] = self.stripe
            self.stripe = self.datstack[-1]
            self.datstack = self.datstack[:-1]
        elif tag in ["report"]:
            ## append the structure to the current stripe
            self.stripe.append(self.struct)
            self.struct = self.datstack[-1]
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
            ## Remember, groupt is in backwards order from
            ## grouph. It sounds strange, but that actually is what I want,
            ## because that's the order in which I'll need them.
            ## so, grouph and groupt get processed the same here.
            if len(self.struct["groupt"]) < len(self.struct["groups"]):
                self.struct["groupt"].append(None)
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
            "skins"  : self.skins,}
        return self.parsed


###################################################
##[ zebra.Generator ]##############################
###################################################
##
## @TODO: Generator should do MUCH  more of the work
##
## I'm thinking that flatten() should be set up more
## like xmllib... it'll have a flatten_report
## (which it has now), flatten_xxx, flatten_yyyyyy
## and then a flatten_unknown which gets called by
## default.
##
## The only reason I'm not doing this now is because
## I'm waiting for the "official" python DOM
## implementation to work itself out, at which point
## I'll want Zebra to use that, and the whole concept
## of what's being flattened will completely change.
##
## besides: I'm almost pretending that the PHP3 stuff
## isn't there, and all we do is python.. :)
##
#####################################################
class Generator:
    reZVar = re.compile("{([$!]?\w+)}", re.I | re.S )

    def __init__(self):
        self.head = ""
        self.foot = ""
    
    def generate(self, parsedict):
        return self.head + self.flatten(parsedict["stripe"]) + self.foot

    
    def flatten(self, stripeset, depth=0, context="show"):
        return ""
    
    def interpolate(self):
        pass

    def flatten_report(self):
        pass


###################################################
## cleanup striped tags if useMessy is turned on ##
###################################################
## @TODO: this doesn't get called anymore! allow useMessy for non-o2x!
## @TODO: account for freestanding <'s (eg, in a script)
## @TODO: *OR* account for <![CDATA[]]>
if (useMessy):
    reTag    = re.compile("(<)([^>]+)(>)", re.I | re.S )
    reClean = re.compile("[!?]|/?z:.*", re.I | re.S )

    def tidy(mess):
        if reClean.match(mess.group(2)):
            return mess.group(0)
        else:
            return "&lt;" + mess.group(2) + "&gt;"

    ## so clean it up already:
    zbr = reTag.sub(tidy, zbr)


###################################################
##[ main code ]####################################
###################################################

if __name__ == "__main__":

    # read in the file, if supplied,
    if len (sys.argv) > 1:
        zbo = open(sys.argv[1]).read()

    # otherwise use stdin
    else:
        zbo = sys.stdin.read()

    # compile it and print the results
    zEngine = Engine()
    #print zEngine.parse(zbo)
    print zEngine.compile(zbo)
