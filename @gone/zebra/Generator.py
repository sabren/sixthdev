"""
Abstract Generator class. Subclass this for language-specific output.

$Id$ 
"""
import re

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
    """Master Generator class. Subclass this for specific languages.

    Specifically, you need to override several abstract methods:

    interpolate_var(self, varname, context)
    interpolate_field(self, fieldname, context)

    flatten(@TODO:)
    flatten_report(@TODO:)

    """
    
    def __init__(self):
        self.head = ""
        self.foot = ""
        self.initialDepth = 0
        self.reZCmd = re.compile(
            r"""
              (\\*)    # count up all the backspaces before the 
                       # {}, so we can tell whether or not it
                       # is being escaped.
                       
              {        # zebra commands start with {
              ([^}]*)  # contain some number of non-} chars
                       # @TODO: allow '\}' inside zebra commands?
              }        # and end with a }
             """,
            re.I | re.S | re.X )

    
    def generate(self, parsedict):
        self.parsedict = parsedict
        return self.head \
               + self.flatten(parsedict["stripe"],context="show") \
               + self.foot

    def interpolate(self, s, context):
        
        """replaces zebra commands in a flattend stripeset..

        today:
        \{..anything..} # ignored
        {fields}
        {$vars}
        {!inserts}

        someday in the far future:
        {@zebraFunctionCall}
        {&nativeFunctionCall}
        {=clientSideScript}
        """

        # we can't pass arbitrary variables to the
        # function that gets called by reZCmd.sub()
        # .. so we're storing it in this special
        # state variable...
        self._interpolationContext = context

        res = self.reZCmd.sub(self._interpolateReplace, s)
        
        return res


    def _interpolateReplace(self, match):
        """A helper function for interpolate(). Don't call it directly."""

        res = ""

        # if there's an odd number of \'s,
        # then we should just ignore this {..} set
        escape = match.group(1)
        if len(escape) % 2 == 1:
            res = escape[:-1] + "{" + match.group(2) + "}"
        else:
            res = escape 
        
            token = match.group(2)

            if token[0]=="!":
                if self.parsedict['named'].has_key(token[1:]):
                    # context="exec" so you don't get: print "print"whatever""
                    # @TODO: maybe have a "passthru" context, as some
                    # languages might alter "exec"?
                    # (eg, php3 mode might one day use "<?" and  "?>"
                    res = res + \
                          self.flatten(self.parsedict['named'][token[1:]],
                                       context="exec")
                else:
                    raise "No stripe named " + token[1:]
            elif token[0] == "$":
                res = res + \
                      self.interpolate_var(token, self._interpolationContext)
            else:
                res = res + \
                      self.interpolate_field(token, self._interpolationContext)
                
        return res

    ## ABSTRACT METHODS #########################################

    def interpolate_var(self, varname, context):
        raise "Abstract method. Subclass it and call that."

    def interpolate_field(self, fieldname, context):
        raise "Abstract method. Subclass it and call that."

    def flatten(self, stripeset, depth=0, context="show"):
        raise "Abstract method. Subclass it and call that."

    def flatten_report(self):
        raise "Abstract method. Subclass it and call that."


