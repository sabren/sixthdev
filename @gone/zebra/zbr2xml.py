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

            ## zebra lines begin with *
            if line[left] == "*":
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

                ## find the end of the block, which should be
                ## less indented than the inside of the block.
                topx = x = x + 1
                newleft = left + 4
                while (x<len(lines)) and (lines[x][:newleft])==(" " * 4):
                    x = x + 1
                    
                ## run this routine recursively on the inner block:
                res = res + self._deBlock(lines[topx:x], tok, attrs, newleft)
                
            ## just a normal line..
            else:
                res = res + line + "\n"

            ## move on to the next line and continue with the while() loop:
            x = x + 1

        ## cap off the current tag and get out of here!
        res = res + "</%s>\n" % tag
        return res


    ## tag handlers #######################################

    def parse_if(self, tokens):
        return 'condition="%s"' % string.join(tokens[1:], " ")

    def parse_for(self, tokens):
        return ""
