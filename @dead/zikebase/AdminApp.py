"""
AdminApp - an actor that uses zebra and zdc to simplify web apps.
"""
__ver__="$Id$"

import weblib, zebra

class AdminApp(weblib.Actor):
    __super = weblib.Actor

    def __init__(self, input=None):
        self.__super.__init__(self, input)
        self.what = {}

    def map_what(self, what):
        return self.what.get("what")

    def enter(self):
        weblib.auth.check()
        zebra.show("dsp_head")

    def exit(self):
        zebra.show("dsp_foot")
    
    def act_list(self):
        """
        generic list routine
        """
        what = self.input.get("what", "")
        if hasattr(self, "list_%s" % what):
            getattr(self, "list_%s" % what)()
        else:
            import zebra
            try:
                self.consult({
                    "list": getattr(self, "qry_%s" % what)()
                    })
            except AttributeError:
                self.complain("self.qry_%s() not defined" % what)
            try:
                zebra.show("lst_%s" % what, self.model)
            except IOError:
                self.complain("unable to load lst_%s" % what)


    def act_show(self):
        """
        generic show routine
        """
        # @TODO: consolidate with act_edit
        what = self.input.get("what", "")
        # allow overriding this without having to change actions:
        if hasattr(self, "show_%s" % what):
            getattr(self, "show_%s" % what)()
        else:
            import zdc
            #@TODO: this ID stuff is just a hack to get categories working.
            #@TODO: there needs to be a generic scheme for doing this..
            if self.input.get("ID"):
                obj = self.map_what(what)(ID=self.input.get("ID"))
            else:
                obj = self.map_what(what)()
                obj.ID = 0
            self.consult(zdc.ObjectView(obj))
            try:
                zebra.show("dsp_%s" % what, self.model)
            except IOError:
                print "[error: dsp_%s template not found]" % what

    def act_edit(self):
        """
        generic object-modifying mechanism
        """
        what = self.input.get("what", "")
        if self.input.get("ID"):
            if hasattr(self, "edit_%s" % what):
                getattr(self, "edit_%s" % what)()
            else:
                import zdc
                zebra.show("frm_%s" % what, zdc.ObjectView(
                    self.map_what(what)(ID=self.input.get("ID"))))
        else:
            self.complain("no ID given")

    def act_create(self):
        """
        generic routine to display a form for adding an object
        """
        what = self.input.get("what", "")
        try:
            if hasattr(self, "create_%s" % what):
                getattr(self, "create_%s" % what)()
            else:
                import zdc
                zebra.show("frm_%s" % what, zdc.ObjectView(
                    self.map_what(what)()))
        except IOError:
            self.complain("frm_%s template not found" % what)
            
    def act_delete(self):
        """
        Generic object-deletion mechanism.
        """
        what = self.input.get("what", "")
        self.objectEdit("delete")
        next = self._whatnext()
        if not next:
            self.do("list", what=what)
        else:
            #@TODO: clean up / clarify this magic side effect.. (_next_)
            self.input = self._next_
            self.do(next)


    def act_save(self):
        """
        Generic object-deletion mechanism.
        """
        what = self.input.get("what", "")
        if hasattr(self, "save_%s" % what):
            getattr(self, "save_%s" % what)()
        else:
            self.objectEdit("save")
        next = self._whatnext()
        if not next:
            self.do("list", what=what)
        else:
            #@TODO: clean up / clarify this magic side effect.. (_next_)
            self.input = self._next_
            self.do(next)

    def objectEdit(self, command):
        """
        generic routine that invokes an ObjectEditor
        and feeds it a command.. Requires that you pass
        a 'what' in on the input string.
        """
        what = self.input.get("what", "")
        klass = self.map_what(what)
        if klass:
            import zikebase
            ed = zikebase.ObjectEditor(klass,
                     self.input.get("ID"), input=self.input)
            ed.do(command)
        else:
            print "don't know how to %s a %s" % (command, what)


    def _whatnext(self):
        _next_ = weblib.request.parse(self.input.get("_next_", ""))
        if _next_.has_key("action"):
            self._next_ = _next_
            return _next_["action"]
