import weblib, zebra

import zikebase
zikebase.load("AdminApp")


class ZikeShopAdminApp(zikebase.AdminApp):
    __super = zikebase.AdminApp

    def enter(self):
        self.__super.enter(self)
        #@TODO: this is a big mistake:
        weblib.auth.user.siteID=1
        

    def objectEdit(self):
        #@TODO: clean this siteID junk up
        self.input["siteID"] = weblib.auth.user.siteID
        self.__super.objectEdit(self)

    def act_save(self):
        #@TODO: get rid of siteID crap
        import zikeshop
        zikeshop.siteID = weblib.auth.user.siteID
        self.__super.save(self)


    ## home page ########################################

    def act_(self):
        print "zikeshop home page"

    ## category stuff ##################################
        
    def list_category(self):
        self.consult("mdl_category")
        zebra.show("lst_category", self.model)


    ## product stuff ###################################

    def list_product(self):
        self.model["nodeID"] = self.input.get("nodeID", 0)
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

    def list_sale(self):
        self.model = self.input
        self.consult("mdl_sale")
        zebra.show("lst_sale", self.model)

    ## inventory stuff #################################

    def act_inventory(self):
        self.consult("mdl_product")
        zebra.show("dsp_inventory", self.model)


    ######### THIS SHOULD BE IN A SUPERCLASS ############


    def map_what(self, what):
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



if __name__=="__main__":
    ZikeShopAdminApp().act()

