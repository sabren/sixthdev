"""
translate zebra's *.zbr files to xml

$Id$
"""
import zebra, string

#####[ Z2X CLASS ]#################################################

class Z2X:
    "Class to translate zebra report files (*.zbr) to xml"

    ## public interface ############################

    def translate(self, zbr):
        "Z2X().translate(zbr) => xml representation of the report"

        ## we deal with the file line by line:
        lines = string.split(zbr, "\n")
        
        ## strip empty string that shows up if \n on last line:
        if lines[-1]=='': lines = lines[:-1]
        
        ## master template:
        res = '<?xml version="1.0"?>\n'
        res = res + self._deBlock(lines,"zebra")
        return res


    ## helper method ###############################

    def _deBlock(self, lines, tag, attrs="", left=0):
        "Recursive routine to handle chunks of ZBR code"

        if attrs:
            res = "<%s %s>\n" % (tag, attrs)
        else:
            res = "<%s>\n" % tag

        x = 0
        while x < len(lines):
            lineNo = x + 1
            
            ## only look from the leftmost position onwards.
            ## (it's okay because we make sure theres' nothing
            ## but space in there a little later..
            line = lines[x][left:]

            ## compress blank lines
            if string.strip(line)=="":
                res = res + "\n"

            ## comments are single lines starting with * #
            elif string.lstrip(string.lstrip(line[1:]))[0:1] == "#":
                # this little mess just strips off the * and #
                res = res + "<rem>%s</rem>\n" \
                      % xmlEncode(string.lstrip(line[1:])[2:])

            ## zebra commands begin with *
            elif string.lstrip(line)[0] == "*":
                line = string.strip(line)

                ## .. and end with : or ;
                if line[-1] == ":":
                    isBlock = 1
                elif line[-1] == ";":
                    isBlock = 0
                else:
                    raise SyntaxError, \
                          "* tag without ':' or ';' on line %i\n[%s]" \
                          % (lineNo, line)
                line = line[:-1]
                
                ## get the tokens after *:
                toks = string.split(line, " ")[1:]
                tok = toks[0]
                
                ## see if we can parse that token:
                if hasattr(self, "parse_"+tok):
                    attrs = apply(getattr(self,"parse_"+tok), (toks,))
                else:
                    raise NameError, \
                          "Don't know how to handle '%s' on line %i" \
                          % (line, lineNo)

                ## find the new left edge:
                if isBlock:
                    newleft = 0
                    topx = x = x + 1
                    if topx >= len(lines):
                        newleft = left - 1
                    else:
                        for i in range(len(lines[topx])):
                            if lines[topx][i]!=" ":
                                newleft = i
                                break

                    ## find the end of the block, which should be
                    ## less indented than the inside of the block.
                    if newleft <= left:
                        ## the block is empty
                        pass
                    else:
                        while (x<len(lines)):
                            if (string.strip(lines[x])=="") \
                               or (lines[x][:newleft])==(" " * newleft):
                                x = x + 1
                            else:
                                break
                    
                    ## run this routine recursively on the inner block:
                    res = res + self._deBlock(lines[topx:x],
                                              tok, attrs, newleft)

                    ## we've already added 1, so jump back to the top:
                    continue


                else:
                    # not a block...
                    res = res + "<%s %s/>\n" % (tok, attrs)
                    
                
            ## just a normal line..
            else:
                res = res + deCurl(xmlEncode(line)) + "\n"

            ## move on to the next line and continue with the while() loop:
            x = x + 1

        ## cap off the current tag and get out of here!
        res = res + "</%s>\n" % tag
        return res


    ## tag handlers #######################################

    def parse_exec(self, tokens):
        return '' # exec has no options (yet)

    def parse_if(self, tokens):
        return 'condition="%s"' % string.join(tokens[1:], " ")

    def parse_ef(self, tokens):
        return 'condition="%s"' % string.join(tokens[1:], " ")

    def parse_el(self, tokens):
        return '' # el has no options (yet)

    def parse_for(self, tokens):
        return 'series="%s"' % tokens[1]

    def parse_none(self, tokens):
        return '' # none has no options

    def parse_head(self, tokens):
        return '' # no options yet

    def parse_foot(self, tokens):
        return '' # no options yet

    def parse_glue(self, tokens):
        return '' # no options yet

    def parse_include(self, tokens):
        return 'file="%s"' % tokens[1]


### HELPER FUNCTIONS ############################################

_entitymap = {
    "<" : "lt",
    ">" : "gt" ,   
    "&" : "amp",      
    }

def xmlEncode(s):
    "Converts <, >, and & to xml entities."
    res = ""
    for ch in s:
        if _entitymap.has_key(ch):
            res = res + "&" + _entitymap[ch] + ";"
        else:
            res = res + ch
    return res


def deCurl(s):
    """
    {abc} => <var>abc</var> 
    {:xyz:} => <expr>xyz</expr>
    
    use backslash to escape.
    eg, \{abc}
    or {: 'this is a \:} string' :}
    """
    import re
    # these don't match newlines cuz there's no re.DOTALL.
    # that's because vars/exprs are single lines only!
    # which is helpful if you've got {'s in your template
    # eg, with javascript on an html page..
    reVar = re.compile(r'(?!\\){\?(.*?)\?}')
    reExpr = re.compile(r'(?!\\){:(.*?)(?!\\):}')
    res = s
    # do xpr first so we don't have to complicate reVar to look for :'s
    res = reExpr.sub('<xpr>\\1</xpr>', res)
    res = reVar.sub('<var>\\1</var>', res)
    return res


if __name__=="__main__":
    import sys
    try:
        file = sys.argv[1]
    except:
        print "reading from stdin.."
        ifp = sys.stdin
    else:
        ifp = open(file, "r")
    print Z2X().translate(ifp.read())
