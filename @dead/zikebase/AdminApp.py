"""
AdminApp - an actor that uses zebra and zdc to simplify web apps.
"""
__ver__="$Id$"

import weblib, zebra

class AppActor(weblib.Actor):

    def enter(self):
        weblib.auth.check()
        zebra.show("dsp_head")

    def exit(self):
        zebra.show("dsp_foot")
    
    def complain(self, problem):
        """
        Prints a pretty error message.
        """
        print '<b>[</b><span style="color:red">error:</span> %s<b>]</b>' \
              % problem

    def consult(self, newModel):
        """
        updates the Actor's internal model based on newModel.
        newModel can be either a module name or a dict.

        if it's a module name, the module should contain
        a dict called model.
        """
        # models and modules.... heh... :)
        if type(newModel) == type(""):
            self.model.update(__import__(newModel).model)
        else:
            # assume it's a dict of sorts:
            for item in newModel.keys():
                self.model[item] = newModel[item]

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
                zebra.show("lst_%s" % what)
            except IOError:
                print "[error: unable to load lst_%s]" % what


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
                obj = self.fetch_class(what)(ID=self.input.get("ID"))
            else:
                obj = self.fetch_class(what)()
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
        if self.input.get("ID"):
            what = self.input.get("what", "")
            import zdc
            zebra.show("frm_%s" % what, zdc.ObjectView(
                self.fetch_class(what)(ID=self.input.get("ID"))))
        else:
            print "[error: no ID given]"
        
    def act_delete(self):
        """
        Generic object-deletion mechanism.
        """
        what = self.input.get("what", "")
        self.objectEdit("delete")
        next = self._whatnext()
        if not next:
            self.perform("lst_%s" % what)
        else:
            #@TODO: clean up / clarify this magic side effect.. (_next_)
            self.input = self._next_
            self.perform(next)


    def act_save(self):
        """
        Generic object-deletion mechanism.
        """
        #@TODO: get rid of siteID crap
        import zikeshop
        zikeshop.siteID = weblib.auth.user.siteID
        what = self.input.get("what", "")
        self.objectEdit("save")
        next = self._whatnext()
        if not next:
            self.perform("lst_%s" % what)
        else:
            #@TODO: clean up / clarify this magic side effect.. (_next_)
            self.input = self._next_
            self.perform(next)

    def objectEdit(self, command):
        """
        generic routine that invokes an ObjectEditor
        and feeds it a command.. Requires that you pass
        a 'what' in on the input string.
        """
        what = self.input.get("what", "")
        klass = self.fetch_class(what)
        if klass:
            import zikebase
            #@TODO: clean this siteID junk up
            self.input["siteID"] = weblib.auth.user.siteID
            ed = zikebase.ObjectEditor(klass,
                     self.input.get("ID"), input=self.input)
            ed.act(command)
        else:
            print "don't know how to %s a %s" % (command, what)

    def act_create(self):
        """
        generic routine to display a form for adding an object
        """
        what = self.input.get("what", "")
        try:
            import zdc
            zebra.show("frm_%s" % what, zdc.ObjectView(
                self.fetch_class(what)()))
        except IOError:
            print "[error: no form to edit %s]" % what

    def _whatnext(self):
        _next_ = weblib.request.parse(self.input.get("_next_", ""))
        if _next_.has_key("action"):
            self._next_ = _next_
            return _next_["action"]
