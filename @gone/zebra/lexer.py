"""
Expression Parser for Zebra

$Id$
"""
import zebra

INT, STR, TUP = type(0), type(""), type(())

def _walk(tree, res):
    "routine to walk the parse tree"
    for node in tree:
        TYP = type(node)
        if TYP==INT:
            try:
                import token
                res.append(token.tok_name[node])
            except KeyError:
                pass
        elif TYP==STR:
            res.append(node)
        elif TYP==TUP:
            _walk(node, res)


def lex(expression):
    "Tokenize the expression by flattening python's own parse tree."
    #@TODO: the tokenize module already does this..
    import parser, symbol
    tree = parser.expr(expression).totuple()
    toks = []
    _walk(tree,toks)

    res = []
    for _ in range(0,len(toks),2):
        res.append(tuple(toks[_:_+2]))

    ## we don't need this junk at the end:
    if res[-2:] == [('NEWLINE',''), ('ENDMARKER', '')]:
        res = res[:-2]

    return res



def validate(tokens):
    "Validation of zebra tokens."
    
    ## this is just a start...

    for token in tokens:
        #>> lambda <<#
        # make sure they don't have lambdas, because we can't
        # easily translate them to other languages.
        if token[0]=="NAME" and token[1]=="lambda":
            raise SyntaxError, "lambdas are not allowed in zebra."
    return tokens


def parse(expression):
    "conveniece function to lex and validate an expression"
    return validate(lex(expression))
    

    
