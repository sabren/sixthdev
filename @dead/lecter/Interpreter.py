"""
the lecter interpreter
"""
__ver__="$Id$"
## eventually we'll break this into a parser and compiler
## with a command loop.. but for now, all the code lives in here.
import lecter
from lecter import TRUE, FALSE
import Wildcard
WILDCARD = Wildcard.Wildcard()
    
class Interpreter:
    def __init__(self):
        self.knowledge = {
            "true/0"  :{():TRUE},
            "false/0" :{():FALSE},
            }

    def parse(self, expr):
        """
        parse a predicate
        """
        paren = expr.find("(")
        if paren >-1:
            if expr[-1]!=")":
                raise SyntaxError, "no closing parens: %s" % expr
            import string
            pred = expr[:paren]
            args = tuple(map(string.strip, expr[paren+1:-1].split(",")))
        else:
            pred = expr
            args = ()
        return pred, args


    def eval(self, code):
        """
        evaluate an assertion or query.
        """
        action = code[-1]
        pred, args = self.parse(code[:-1])
        key = pred + "/" + str(len(args))

        if action=="?":       # query
            dict=self.knowledge.get(key,None)
            if dict is None:
                raise NameError, "unknown predicate: %s" % pred
            else:
                pattern = []
                ismatch = 0
                for arg in args:
                    if arg[0]=="$": # variables
                        ismatch = 1
                        pattern.append(WILDCARD)
                    else:
                        pattern.append(arg)
                pattern = tuple(pattern)

                if ismatch:
                    matches = []
                    for key in dict.keys():
                        if key == pattern:
                            dict = {}
                            for i in range(len(args)):
                                dict[args[i]]=key[i]
                            matches.append(dict)
                    return tuple(matches)
                else:
                    return dict.get(pattern,FALSE)

        elif action==".":     # assertion
            self.knowledge.setdefault(key,{})[args] = TRUE
        else:
            raise SyntaxError, "unknown action: %s" % code

