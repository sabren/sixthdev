"""
fake data for testing Zikeshop

$Id$
"""

def load():
    import zdc, zikeshop, zikebase
    from sqlTest import dbc
    
    dbc.cursor().execute("DELETE FROM base_user")
    dbc.cursor().execute("DELETE FROM base_node")
    dbc.cursor().execute("DELETE FROM shop_product")
    dbc.cursor().execute("DELETE FROM shop_product_node")


    user = zikebase.User()
    user.username=user.uid=user.email="username"
    user.password="password"
    user.siteID=1
    user.save()

    user = zikebase.User()
    user.username=user.uid=user.email="michal"
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



if __name__=="__main__":
    load()
