"""
Bootstrap compiler for Zebra.
"""
__ver__="$Id$"

# @TODO: how about a "* set" tag?

import zebra
import xml2mdl

class Bootstrap:
    "A class to compile zebra reports until zebra can compile itself."

    parserClass = xml2mdl.X2M


    def toObject(self, zbx):
        "bstrap.toObject(zbx) => a python Report object"

        exec(self.compile(zbx))
        return Report()


    def parse(self, zbx):
        "Returns a Model-style representation of zbx"

        parser = self.parserClass()
        parser.feed(zbx)
        return parser.model


    def compile(self, zbx):
        "Bootstrap.().compile(zbx) => python code for zbx"

        return self.walk(self.parse(zbx))


    def walk(self, model, mode="show"):
        "Walks along the model, converting it to code..."
        import types

        res = ""

        for item in model:
            ## XML tags are represented as dicts
            if type(item) == types.DictType:

                ## do we have a handler for the tag?
                if not hasattr(self, "handle_" + item["__tag__"]):
                    raise NameError, \
                          "Don't know how to handle <%s>" % item["__tag__"]

                res = res + apply(getattr(self, "handle_" + item["__tag__"]),
                                  (item["__data__"], item))
            

            ## CDATA is represented as strings
            elif type(item) == types.StringType:

                ## strip first and last newlines, if present
                if item and item[0]=="\n": item = item[1:]
                if item and item[-1]=="\n": item = item[:-1]

                if item:
                    if mode=="show":
                        res = res + "zres = zres + '%s'\n" \
                              % zebra.escape(item)
                    else:
                        res = res + item
            
            else:
                raise TypeError, \
                      "Don't know how to cope with %s" % type(item)
        return res


## @TODO: probably get rid of this..
## though, it might come in handy if trying to get zebra to work with
## a really strict language... (but why do that?)

##     ## language-specific templates for handling scope ##############

##     def scopify(self, expression):
##         "points names in expressions to the current scope"
##         import string, keyword
##         res = []
##         toks = zebra.lexer.parse(string.strip(expression))
##         for token in toks:
##             if token[0]=="NAME" and not keyword.iskeyword(token[1]):
##                 res.append("scope.get('%s','')" % token[1])
##             else:
##                 res.append(token[1])
##         return string.join(res, " ")



    ## individual tag templates ####################################

    def handle_zebra(self, model, attrs):
        res = zebra.trim(
            '''
            class Report:
            
                def show(self, model={}):
                    print self.fetch(model)

                def fetch(self, model={}):
                    import copy   # used for pushing scope onto stack

                    scope = globals()
                    # This scope thing is so that we can generate
                    # code that says:
                    #
                    #         zres = zres + x
                    # *OR*
                    #         zres = zres + scope.get(x, '')
                    #
                    # It also actually does variable scoping,
                    # when combined with scope_stack, below.
                    #
                    # I wanted to use scope=locals(), but
                    # then the 'zres + x' wouldn't work.
                    # @TODO: is this scope scheme threadsafe?
                    
                    scope_stack = []

                    # scope.update(model), but model might be a UserDict:
                    for item in model.keys():
                        scope[item] = model[item]

                    # zres is the result (the output we're building)
                    zres = ""
            ''')
        res = res + zebra.indent(self.walk(model), 2)
        res = res + zebra.trim(
            ''' 
            # end of Report.fetch()
                    return zres

            def fetch(model={}):
                return Report().fetch(model)
                
            def show(model={}):
                return Report().show(model)
            ''')
        return res

    def handle_rem(self, model, attrs):
        return "" # @TODO: do we want comments after compliation?


    def handle_for(self, model, attrs):
        res = zebra.trim(
            '''
            _ = 0
            _max_ = len(scope["%(series)s"])
            for _ in range(_max_):
                # handle scope inside the loop in case we have
                # recursive names (eg, children->children->children)
                scope_stack.append(copy.copy(scope))
                
                # can't do .update if it's a UserDict:
                mdl = scope["%(series)s"][_]
                for item in mdl.keys():
                    scope[item]=mdl[item]
            ''' % attrs)
        res = res + zebra.indent(self.walk(model), 1)            
        res = res + zebra.trim(
            '''
            #   ## close for-%(series)s loop ##########
                globals().update(scope_stack.pop())
            ''' % attrs)
        return res

    def handle_none(self, model, attrs):
        res = "if not _max_:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res


    def handle_var(self, model, attrs):
        res = "zres = zres + str(scope.get('%s',''))\n" % model[0]
        return res

    def handle_xpr(self, model, attrs):
        res = "zres = zres + str(%s)\n" \
              % self.walk(model, mode="exec")
        return res

    def handle_exec(self, model, attrs):
        res = "globals().update(scope)\n" \
              + self.walk(model, mode="exec") + "\n" \
              + "scope.update(globals())\n" \
              + "scope.update(locals())\n"
        return res


    def handle_if(self, model, attrs):
        res = "if %s:\n" % attrs["condition"]
        res = res + zebra.indent(self.walk(model), 1)
        return res


    def handle_ef(self, model, attrs):
        res = "elif %s:\n" % attrs["condition"]
        res = res + zebra.indent(self.walk(model), 1)
        return res

    def handle_el(self, model, attrs):
        res = "else:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res

    def handle_nl(self, model, attrs):
        return 'zres = zres + "\\n"\n'

    def handle_head(self, model, attrs):
        # @TODO: handle grouped heads
        res = "if _ == 0:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res

    def handle_body(self, model, attrs):
        "the body tag does nothing at all.. it's purely aesthetic"
        return self.walk(model)

    def handle_foot(self, model, attrs):
        # @TODO: handle grouped feet
        res = "if _ + 1 == _max_:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res

    def handle_glue(self, model, attrs):
        res = "if _ + 1 < _max_:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res

    def handle_include(self, model, attrs):
        res = "import zebra\n"
        res = res + "zres=zres + zebra.fetch('%s',scope)\n" % attrs["file"]

        # @TODO: include shouldn't depend on zebra!
        #res = res + "zres = zres+ %s.fetch(scope)\n" % attrs["module"]
        return res
