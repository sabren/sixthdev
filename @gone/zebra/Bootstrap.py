"""
Bootstrap compiler for Zebra.

$Id$
"""
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


    def walk(self, model):
        "Walks along the model, converting it to code..."
        import types

        res = ""

        for item in model:
            ## XML tags are represented as dicts
            if type(item) == types.DictType:

                ## do we have a handler for the tag?
                assert hasattr(self, "handle_" + item["__tag__"]), \
                       "Don't know how to handle <%s>" % item["__tag__"]

                res = res + apply(getattr(self, "handle_" + item["__tag__"]),
                                  (item["__data__"], item))
            

            ## CDATA is represented as strings
            elif type(item) == types.StringType:

                ## strip first and last newlines, if present
                if item and item[0]=="\n": item = item[1:]
                if item and item[-1]=="\n": item = item[:-1]

                if item:
                    res = res + "zres = zres + '%s'\n" \
                          % zebra.escape(item)
            
            else:
                raise TypeError, \
                      "Don't know how to cope with %s" % type(item)
        return res


    ## individual tag templates ####################################

    ## <zebra> ##
    def handle_zebra(self, model, attrs):
        res = zebra.trim(
            """
            class Report:
            
                def show(self, model={}):
                    print self.fetch(model)

                def fetch(self, model={}):
                    self.model = model
                    globals().update(self.model)
                    zres = ""
            """)
        res = res + zebra.indent(self.walk(model), 2)
        res = res + zebra.trim(
            """
            # end of Report.fetch()
                    return zres

            def fetch(model={}):
                Report().fetch(model)
                
            def show(model={}):
                Report().show(model)
            """)
        return res


    ## <for> ##
    def handle_for(self, model, attrs):
        res = zebra.trim(
            """
            _ = 0
            _max_ = len(self.model["%s"])
            for _ in range(_max_):
                #@TODO: take this out of the global namespace.
                #(either figure out why local doesn't work, or
                #just wrap it all in an exec()
                globals().update(self.model["%s"][_])
            """ % (attrs["series"], attrs["series"]))
        res = res + zebra.indent(self.walk(model), 1)            
        res = res + zebra.trim(
            """
            del _
            """)
        return res


    ## <none> ##
    def handle_none(self, model, attrs):
        res = "if not _max_:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res


    ## <var> ##
    def handle_var(self, model, attrs):
        res = "zres = zres + str(%s)\n" % model[0]
        return res


    ## <if> ##
    def handle_if(self, model, attrs):
        res = "if %s:\n" % attrs["condition"]
        res = res + zebra.indent(self.walk(model), 1)
        return res


    ## <ef> ##
    def handle_ef(self, model, attrs):
        res = "elif %s:\n" % attrs["condition"]
        res = res + zebra.indent(self.walk(model), 1)
        return res


    ## <el> ##
    def handle_el(self, model, attrs):
        res = "else:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res


    ## <br> ##
    def handle_br(self, model, attrs):
        return 'zres = zres + "\\n"\n'


    ## <head> ##
    def handle_head(self, model, attrs):
        # @TODO: handle grouped heads
        res = "if _ == 0:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res

    ## <foot> ##
    def handle_foot(self, model, attrs):
        # @TODO: handle grouped feet
        res = "if _ + 1 == _max_:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res


    ## <glue> ##
    def handle_glue(self, model, attrs):
        res = "if _ + 1 < _max_:\n"
        res = res + zebra.indent(self.walk(model), 1)
        return res
