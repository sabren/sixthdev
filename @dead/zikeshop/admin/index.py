import weblib, zebra
import zikebase
zikebase.load("AdminApp")

def popupHelp(msg):
    res = '<a href="#" onclick="alert(\'%s\')">[?]</a>' % msg
    return res

class ZikeShopAdminApp(zikebase.AdminApp):
       
    ## home page ########################################

    def act_(self):
        self.list_category()

    def enter(self):
        self.model["popupHelp"] = popupHelp
        zebra.show("dsp_head",self.model)

    def exit(self):
        zebra.show("dsp_foot",self.model)
        
    ## category stuff ##################################
        
    def list_category(self):
        self.consult("mdl_category")
        zebra.show("lst_category", self.model)


    ## product stuff ###################################

    def list_product(self):
        # we want to see products in a particular node
        # (or in no nodes at all)
        nID = self.model["nodeID"] = int(self.input.get("nodeID", 0))
        import mdl_product
        mdl_product.nodeID = nID
        mdl_product.doit()
        if nID:
            self.model["path"] = zikebase.Node(ID=self.model["nodeID"]).path
        self.consult(mdl_product.model)
        self.consult("mdl_category")
        zebra.show("lst_product", self.model)

    def save_product(self):
        # hold must not be null..
        if not self.input["hold"]:
            self.input["hold"] = 0
        self.generic_save("product")
        self.redirect(action="show&what=product&ID=%s" % self.objectID)

    ## style stuff ######################################
    def create_style(self):
        try:
            prod = zikeshop.Product(ID=int(self.input["productID"]))
        except:
            self.complain("unable to create style for product #%s" \
                          % self.input["productID"])
        else:
            self.input["price"]=str(prod.price)
            self.generic_create("style")
    
    def save_style(self):
        self.generic_save("style")
        self.redirect(action="show&what=product&ID=%s" %
                      self.input.get('parentID'))
        

    ## sale stuff ######################################

    def show_sale(self):
        #@TODO: zebrafy this (not until zebra can cope with 1:1 rels.)
        import dsp_sale 

    def act_new_sale(self):
        #@TODO: come up with a real standard for new/adm/edit/whatever actions
        self.model = self.input
        import mdl_product; mdl_product.doit() #@TODO: FIX THIS!!
        self.consult("mdl_product")
        zebra.show("frm_sale", self.model)

    def save_sale(self):
        sed = zikeshop.SaleEditor(zikeshop.Sale, self.input.get("ID"))
        import zdc
        # new sales get a timestamp:
        if not self.input.get("ID"):
            sed.input["tsSold"] = zdc.TIMESTAMP
        sed.act("save")

    def list_sale(self):
        self.model = self.input
        self.consult("mdl_sale")
        self.model["includeFilled"]=int(self.input.get("includeFilled",0))
        self.model["isSearch"]=0
        zebra.show("lst_sale", self.model)

    ######### THIS SHOULD BE IN A SUPERCLASS ############

    def map_what(self, what):
        """
        returns a class to work with based on
        the string passed in. override this!
        """
        res = None
        import zikeshop
        if what == "category":
            res = zikeshop.Category
        elif what=="product":
            res = zikeshop.Product
        elif what=="sale":
            res = zikeshop.Sale
        elif what=="style":
            res = zikeshop.Style
        return res


if __name__=="__main__":
    ZikeShopAdminApp().act()

