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
            ## only look from the leftmost position onwards.
            ## (it's okay because we make sure theres' nothing
            ## but space in there a little later..
            line = lines[x][left:]

            ## compress blank lines
            if string.strip(line)=="":
                res = res + "\n"

            ## zebra lines begin with *
            elif string.lstrip(line)[0] == "*":
                line = string.strip(line)

                ## .. and end with :
                assert line[-1] == ":", \
                       "* tags must end with ':'"
                line = line[:-1]
                
                ## get the tokens after *:
                toks = string.split(line, " ")[1:]
                tok = toks[0]
                
                ## see if we can parse that token:
                if hasattr(self, "parse_"+tok):
                    attrs = apply(getattr(self,"parse_"+tok), (toks,))
                else:
                    raise "Don't know how to handle '%s' on line %i" \
                          % (line, x+1)

                ## find the new left edge:
                topx = x = x + 1
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
                    while (x<len(lines)) \
                          and (lines[x][:newleft])==(" " * newleft):
                        x = x + 1
                    
                ## run this routine recursively on the inner block:
                res = res + self._deBlock(lines[topx:x], tok, attrs, newleft)

                ## we've already added 1, so jump back to the top:
                continue
                
            ## just a normal line..
            else:
                res = res + deVar(xmlEncode(line)) + "\n"

            ## move on to the next line and continue with the while() loop:
            x = x + 1

        ## cap off the current tag and get out of here!
        res = res + "</%s>\n" % tag
        return res


    ## tag handlers #######################################

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


def deVar(s):
    "converts {} to <var> tags. use backslash to escape."
    res = ""
    esc = 0
    for ch in s:
        if esc:
            res = res + ch
            esc = 0
        elif ch == "\\":
            esc = 1
        elif ch=="{":
            res = res + "<var>"
        elif ch=="}":
            res = res + "</var>"
        else:
            res = res + ch
    return res


