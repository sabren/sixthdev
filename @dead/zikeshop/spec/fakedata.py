"""
fake data for testing Zikeshop

$Id$
"""

def load():
    import zdc, zikeshop, zikebase
    from sqlTest import dbc

    ## clear out old data..
    dbc.cursor().execute("DELETE FROM base_user")
    dbc.cursor().execute("DELETE FROM web_sess")
    dbc.cursor().execute("DELETE FROM base_node")
    dbc.cursor().execute("DELETE FROM shop_product")
    dbc.cursor().execute("DELETE FROM shop_product_node")
    dbc.cursor().execute("DELETE FROM shop_style")
    dbc.cursor().execute("DELETE FROM shop_location")
    dbc.cursor().execute("DELETE FROM shop_inventory")

    ## set up a location
    dbc.cursor().execute("INSERT INTO shop_location (name, siteID) "
                         "VALUES ('main location', 1)")

    user = zikebase.User()
    user.username=user.uid=user.email="username"
    user.password="password"
    user.siteID=1
    user.save()

    user = zikebase.User()
    user.username=user.uid=user.email="michal@sabren.com"
    user.password="michal"
    user.siteID=2
    user.save()

    for n in ("toys", "books", "electronics", "games", "michal's stuff"):
        node = zikebase.Node()
        node.name=n
        node.descript=""
        node.siteID=1
        node.save()


    node = zikebase.Node(name="games")
    node.parentID=1
    node.siteID=1
    node.save()


    ## MY NODE ##################################
    node = zikebase.Node(name="michal's stuff")
    node.siteID=2
    node.save()


    ## PRODUCTS#################################

    for p in (("DIC00", "dictionary", "defines words", (2,)),
              ("GUN00", "ray gun", "shoots people", (1,3)),
              ("GAM00", "monopoly", "get rich quick", (4,)),
              ("GAM01", "candyland", "an old game", (4,)),
              ("GAM02", "chess", "an ancient game", (4,)),
              ("PDA00", "palm pilot", "stores stuff", (3,)),

              ("COOKI", "a scary cookie", "oh the horror!", (5,), 2),
              ("FIDO!", "doggy", "a glowing alien slime beast and his little doggy.",
                       (5,), 1),
              ("SKULL", "Self portrait", "a self portrait of the developer, " + \
               "as seen through rose colored X-Ray glasses.", (5,), 3)):

        prod = zikeshop.Product()
        prod.code=p[0]
        prod.name=p[1]
        prod.price=5.00 # everything's five bucks!
        prod.descript=p[2]
        if len(p)>4:
            prod.siteID=2
            prod.pictureID = p[4]
        else:
            prod.siteID=1
        prod.nodeIDs=p[3]
        prod.save()

        ## set up 10 of each product in inventory..
        if prod.name == "dictionary":
            # dictionary has two styles:
            style = zikeshop.Style(productID=prod.ID)
            style.style = "Webster"
            style.save()
            dbc.cursor().execute("INSERT INTO shop_inventory "
                                 "(locationID, styleID, amount) "
                                 "VALUES (1, %i, 5)" % style.ID)
            # and add another:
            style = zikeshop.Style()
            style.productID=prod.ID
            style.style = "Oxford"
            style.save()
            dbc.cursor().execute("INSERT INTO shop_inventory "
                                 "(locationID, styleID, amount) "
                                 "VALUES (1, %i, 5)" % style.ID)
            
        else:
            # everything else has only one style:
            style = zikeshop.Style(productID=prod.ID)
            dbc.cursor().execute("INSERT INTO shop_inventory "
                                 "(locationID, styleID, amount) "
                                 "VALUES (1, %i, 10)" % style.ID)
            

if __name__=="__main__":
    load()