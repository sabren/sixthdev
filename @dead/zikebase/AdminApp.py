"""
AdminApp - an actor that uses zebra and zdc to simplify web apps.
"""
__ver__="$Id$"

import weblib, zebra

class AdminApp(weblib.Actor):
    __super = weblib.Actor

    def __init__(self, input=None):
        self.__super.__init__(self, input)
        #@TODO: just make 'whatmap' into a dict, and get .what from input
        self.what = {}

    def map_what(self, what=None):
        if what is None:
            return self.what.get(self.input.get("what"))
        else:
            return self.what.get(what)


    ## list ###################################################
    
    def act_list(self):
        """
        calls list_{:what:} if defined, else generic_list
        """
        what = self.input.get("what", "")
        if hasattr(self, "list_%s" % what):
            getattr(self, "list_%s" % what)()
        else:
            self.generic_list(what)

    def generic_list(self, what):
        """
        """
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



    ## show ######################################################

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
            self.generic_show(what)

    def generic_show(self, what):
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
            self.complain("dsp_%s template not found]" % what)

    ## edit ########################################################

    def act_edit(self):
        """
        generic object-modifying mechanism
        """
        what = self.input.get("what", "")
        if self.input.get("ID"):
            if hasattr(self, "edit_%s" % what):
                getattr(self, "edit_%s" % what)()
            else:
                self.generic_edit(what)
        else:
            self.complain("no ID given")

    def generic_edit(self, what):
        import zdc
        self.consult(self.input)
        self.consult(zdc.ObjectView(
            self.map_what(what)(ID=self.input.get("ID"))))
        zebra.show("frm_%s" % what, self.model)

    ## create #######################################################

    def act_create(self):
        """
        generic routine to display a form for adding an object
        """
        what = self.input.get("what", "")
        try:
            if hasattr(self, "create_%s" % what):
                getattr(self, "create_%s" % what)()
            else:
                self.generic_create(what)
        except IOError:
            self.complain("frm_%s template not found" % what)

    def generic_create(self, what):
        import zdc
        self.consult(zdc.ObjectView(
            self.map_what(what)()))
        self.consult(self.input) # goes second so we can modify via input..
        zebra.show("frm_%s" % what, self.model)


    ## delete ######################################################
            
    def act_delete(self):
        """
        Generic object-deletion mechanism.
        """
        what = self.input.get("what", "")
        self.objectEdit("delete")
        self.next = ("list", {"what":what})


    ## save ########################################################

    def act_save(self):
        """
        Generic object-deletion mechanism.
        """
        what = self.input.get("what", "")
        if hasattr(self, "save_%s" % what):
            getattr(self, "save_%s" % what)()
        else:
            self.generic_save(what)
        if not self.next:
            self.next = ("list", {"what":what})

    def generic_save(self, what):
        self.objectEdit("save")


    ###[helper method]##############################################

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


