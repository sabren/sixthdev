import weblib, zebra

import zikebase
zikebase.load("AppActor")

class ZikeShopAppActor(zikebase.AppActor):

    def _whatnext(self):
        _next_ = weblib.request.parse(self.input.get("_next_", ""))
        if _next_.has_key("action"):
            self._next_ = _next_
            return _next_["action"]

    def enter(self):
        weblib.auth.check()
        zebra.show("dsp_head")

    ## home page ########################################

    def act_(self):
        print "zikeshop home page"

    ## category stuff ##################################
        
    def act_lst_category(self):
        self.consult("mdl_category")
        zebra.show("lst_category", self.model)


    ## product stuff ###################################

    def act_lst_product(self):
        self.model = self.input
        self.consult("mdl_product")
        self.consult("mdl_category")
        zebra.show("lst_product", self.model)

    ## sale stuff ######################################

    def show_sale(self):
        #@TODO: zebrafy this (not until zebra can cope with 1:1 rels.)
        import dsp_sale 

    def act_new_sale(self):
        #@TODO: come up with a real standard for new/adm/edit/whatever actions
        self.model = self.input
        self.consult("mdl_product")
        zebra.show("frm_sale", self.model)

    def act_lst_sale(self):
        self.model = self.input
        self.consult("mdl_sale")
        zebra.show("lst_sale", self.model)

    ## inventory stuff #################################

    def act_inventory(self):
        self.consult("mdl_product")
        zebra.show("dsp_inventory", self.model)


    ######### THIS SHOULD BE IN A SUPERCLASS ############


    def fetch_class(self, what):
        """
        returns a class to work with based on
        the string passed in. override this!
        """
        res = None
        import zikeshop
        if what == "category":
            import zikebase
            res = zikebase.Node
        elif what=="product":
            res = zikeshop.Product
        elif what=="sale":
            res = zikeshop.Sale
        elif what=="style":
            res = zikeshop.Style
        return res


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

    def exit(self):
        zebra.show("dsp_foot")


if __name__=="__main__":
    ZikeShopAppActor().act()

