from zebra import Generator
import types, string

###################################################
##[ zebra.PHPGenerator ]###########################
###################################################

class PHPGenerator(Generator):
    def __init__(self):
        self.head = "<?\n"
        self.foot = "?>\n"


    def flatten(self, stripeset, depth=0, context="show"):
        """Converts a stripe or stripeset into a string"""

        res = ""
        if type(stripeset)!=types.ListType:
            stripeset = [stripeset]

        for stripe in stripeset:
            stripehead  = stripebody  = stripefoot  = ""
            test = conditional = ""
            if type(stripe)==types.StringType:
                ## strip leading and trailing newlines
                if stripe[0] == "\n":
                    stripe = stripe[1:]
                if stripe[-1] == "\n":
                    stripe = stripe[:-1]
                ## deal with context (we only care when it's a string)
                if (context == "show"):
                    stripehead = 'print "'
                    stripebody = string.replace(
                        string.replace(stripe, '"', '\\"'),
                        "\n", "\\n")
                    stripefoot = '";'
                elif context == "exec":
                    stripebody = stripe
                else:
                    #@TODO: this should raise an error
                    pass
            elif type(stripe)==types.ListType:
                stripebody = self.flatten(stripe,depth+1)
            elif type(stripe)==types.DictionaryType:
                # @TODO: this ought to all be stored in a
                # dictionary that maps tags to functions
                tag = stripe["tag"]
                if tag == "stripe":
                    stripebody = self.flatten(stripe["content"],depth+1,
                                              stripe["context"])[:-1]
                    test   = stripe["test"]
                    conditional = stripe["conditional"]
                elif tag == "report":
                    res = res + self.flatten_report(stripe, depth+1)
                else:
                    print "*** don't know how to flatten " + tag
            else:
                raise("unknown structure in stripe")

            ## finally, the conditional
            if (test) and not (conditional):
                conditional = "if"
            if (test) or (conditional): # el has no condition
                conditionals = {"if":"if", "ef":"elseif", "el":"else"}
                if conditional == "":
                    conditional = "if"
                if conditional in ["if", "ef"]:
                    stripehead = conditionals[conditional] + " (" \
                                 + test + "){\n" \
                                 + "   " + stripehead
                    stripefoot = stripefoot + "\n}"
                elif conditional == "el":
                    stripehead = conditionals[conditional] + " {" \
                                 + "   " + stripehead
                    stripefoot = stripefoot + "\n}"

            res = res + stripehead + stripebody + stripefoot + "\n"

        # now that we have the whole set, interpolate variables:
        res = self.reZVar.sub(self.interpolate, res)
        return res

    ###############################################

    def flatten_report(self, report, depth=0):

        # @TODO: this is one serious kludge.
        # @TODO: code each variable name with depth so can have nested reports
        res = ""
        res = res + \
              "$__db = new " + report["source"] + ";\n" + \
              "$__db->query(\"" + self.flatten(report["query"], context="exec") + "\");\n"

        ## set up two arrays for handling groups
        res = res + "$__groups=array('all'"
        buf = "$__showFoot=array(0"
        for g in report["groups"]:
            res = res + ", '" + g + "'"
            buf = buf + ",0"
        res = res + ");\n"
        res = res + buf + ");\n"

        ## now do the test:
        res = res + "if ($__db->next_record()) {\n";

        ## if there's records, show the head:
        res = res + "   " + self.flatten(report["head"],depth,"show")

        ## nr is next record, tr = this one, pr = previous
        ## we need to look at 3 records at once in order to
        ## know when to print the headers and footers..
        res = res + \
              "   $__nr = $__db->Record;\n" + \
              "   while (($__more = $__db->next_record()) or (! $__nomore)){\n" + \
              "      $__tr = $__nr;\n" + \
              "      if ($__more) { $__nr = $__db->Record; }\n" + \
              "      else { $__nomore = 1; }\n"

        ## handle the grouping for the heads:
        for i in range(len(report["groups"])):
            if report["grouph"][i]:
                res = res + \
                      "      if ($__tr[\"" + report["groups"][i] + "\"] != $__pr[\"" + \
                      report["groups"][i] + "\"]){\n" + \
                      "         " + self.flatten(report["grouph"][i],depth,"show") + \
                      "         unset($__pr);\n" + \
                      "      }\n"

        ## now the body:
        res = res + "      " + self.flatten(report["body"],depth,"show")

        ## and the feet:
        ## .. use a while loop because they're faster than for loops in php3
        res = res + \
              "      if ($__nomore) { $__showFoot[0] = 1; }\n" + \
              "      $__g=1; while ($__g < sizeof($__showFoot)){ \n" + \
              "         if (($__nr[$__groups[$__g]] != $__tr[$__groups[$__g]]) " + \
              "or ($__showFoot[$__g-1])){\n" + \
              "            $__showFoot[$__g] = 1;\n" + \
              "         } else {\n" + \
              "            $__showFoot[$__g] = 0;\n" + \
              "         }\n" + \
              "         $__g++;\n" + \
              "      }\n"

        for i in range(len(report["groups"])):
            if report["groupt"][i]:
                res = res + \
                      "      if ($__showFoot[" + `i+1` + "]){\n" + \
                      "         " + self.flatten(report["groupt"][i],depth,"show") + \
                      "      }\n"

        ## cap off the loop, show the foot...
        res = res + \
              "      $__pr = $__tr;\n" + \
              "   }\n" + \
              "   " + self.flatten(report["foot"],depth,"show")

        ## handle "none"
        if report["none"]:
            res = res + \
                  "} else {\n" + \
                  self.flatten(report["none"],depth,"show")
        res = res + "}\n"

        ## finally, encode variables with depth, so we can nest reports
        reDepth = re.compile("(\$__\w+)", re.I | re.S )
        res = reDepth.sub(r"\1_" + `depth`,res)

        return res



    ###############################################

    def _interpolate(self, match):

        """replaces {fields}, {$vars} and {!inserts}
        in a flattened zebra stripeset..."""

        #@TODO: this is all hard-coded for PHP3. make it generic.
        #@TODO: interpolation needs to be table driven so that
        # we can translate into different languages
        # (or maybe an overridable function?)
        # also, it ought to be per-stripe (and only used on stripe
        # bodies and conditionals)
        # .. that way, we can change interpolation as context changes.

        token = match.group(1)
        if token[0]=="!":
            if self.named.has_key(token[1:]):
                # context="exec" so you don't get: print "print"whatever""
                # @TODO: maybe have a "passthru" context, as some
                # languages might alter "exec"?
                # (eg, php3 mode might one day use "<?" and  "?>"
                return self.flatten(self.named[token[1:]], context="exec")
            else:
                return ""
        elif token[0] == "$":
            return token
        else:
            # fields.. there needs to be a standard
            # way of doing this per language.
            return '$__tr[' + token + ']';


