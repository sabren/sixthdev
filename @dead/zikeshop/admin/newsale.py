import header
import weblib
import zikeshop

weblib.auth.check()


if weblib.request.get("action")=="save":

    ## save the new sale:
    sale = zikeshop.Sale()
    sale.customerID = 0
    sale.ship_addressID = 0
    sale.bill_addressID = 0
    sale.cardID = 0
    sale.shiptypeID = 0
    sale.statusID = zikeshop.Status(status="complete").ID
    sale.siteID = weblib.auth.user.siteID

    cur = zikeshop.dbc.cursor()

    ## calculate the subtotal
    import string
    quantity = {}
    sale.subtotal = zikeshop.FixedPoint("0.00")
    for item in weblib.request.keys():
        if (item[:4] == "qty_") and weblib.request[item]:
            prodID, styleID = string.split(item, "_")[1:]
            quantity[styleID] = int(weblib.request[item])
            sale.subtotal = sale.subtotal + \
                            ( zikeshop.Product(ID=prodID).price \
                              * quantity[styleID])

    ## calculate sales tax.
    store = zikeshop.Store(ID=zikeshop.siteID)
    sale.salestax = store.calcSalesTax(store.address, sale.subtotal)


    # @TODO: add some generic validation routines to weblib (date, number, etc)
    try:
        sale.adjustment = zikeshop.FixedPoint(weblib.request["adjustment"])
    except:
        sale.adjustment = zikeshop.FixedPoint(0)

    try:
        sale.shipping = zikeshop.FixedPoint(weblib.request["shipping"])
    except:
        sale.shipping = zikeshop.FixedPoint(0)
            
    sale.total = str(sale.subtotal + sale.salestax + \
                     sale.shipping + sale.adjustment)
    sale.subtotal = str(sale.subtotal)
    sale.salestax = str(sale.salestax)
    sale.shipping = str(sale.shipping)
    sale.adjustment = str(sale.adjustment)
    sale.siteID = weblib.auth.user.siteID
    sale.save()

    import zdc
    for styleID in quantity.keys():
        style = zikeshop.Style(ID=styleID)
        prod = zikeshop.Product(ID=style.productID)
        cur.execute(
            """
            INSERT INTO shop_sale_item (saleID, styleID, item, quantity, price)
            VALUES (%i, %i, '%s {%s}', %i, %s)
            """ \
            % (sale.ID, style.ID, prod.name, weblib.deNone(style.style),
               quantity[styleID], str(prod.price))
            )


        #@TODO: handle inventory for multiple locations!
        #@TODO: one central inventory decreaser..
        rec = zdc.Record(zdc.Table(zikeshop.dbc, "shop_inventory"),
                         styleID=style.ID)
        rec["amount"] = rec["amount"] - quantity[styleID]
        rec.save()
        
                    

    ## now show the sale:
    del weblib.request["action"]
    weblib.request.form["saleID"] = sale.ID
    import sale
    
else:
    ## show the point-of-sale form:
    
    cur = zikeshop.dbc.cursor()
    sql = "SELECT ID, code, name, price FROM shop_product " \
          "WHERE siteID=%i ORDER BY code" \
          % weblib.auth.user.siteID
    cur.execute(sql)

    print '<h1>enter a new sale</h1>'

    print '<form action="newsale.py" method="post">'

    print '<table border="1">'
    print '<tr><th>code</th><th>product</th><th>price</th>'
    print '<th>quantity</th></tr>'
    for row in cur.fetchall():
        print '<tr>'
        print '<td valign="top">%s</td>' % row[1]
        print '<td valign="top">%s</td>' % row[2]
        print '<td valign="top">%s</td>' % row[3]

        sql = "SELECT ID, style from shop_style WHERE productID=%i " \
              "ORDER BY style" % row[0]
        print '<td align="right">'
        cur.execute(sql)
        for style in cur.fetchall():
            print '%s: <input type="text" size="5" name="qty_%i_%i"><br>' \
                  % (weblib.deNone(style[1]), row[0], style[0])
        print '</td>'
        print '</tr>'
    print '</table>'
    print 'shipping: '
    print '<input type="text" size="5" name="shipping" value="0.00"><br>'
    print 'adjustment: '
    print '<input type="text" size="5" name="adjustment" value="0.00">'
    print ' (eg: "-2.00"  takes $2 off price) <br>'
    print 'charge sales tax: '
    print '<input type="checkbox" name="usetax" value="yes" checked><br>'

    print '<input type="submit" name="action" value="save">'
    print '</form>'

