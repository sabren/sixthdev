"""
AppActor - an actor that uses zebra and zdc to simplify web apps.
"""
__ver__="$Id$"

import weblib, zebra

class AppActor(weblib.Actor):
    
    def enter(self):
        if not getattr(self, "model"):
            self.model={}
    
    def complain(self, problem):
        print "[error: %s]" % problem

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
