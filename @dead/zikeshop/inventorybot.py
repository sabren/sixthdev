import zikeshop
import smtplib

cur = zikeshop.dbc.cursor()
import sqlZike
cur = sqlZike._d_b_c.cursor()
cur.execute(
    """
    SELECT p.name, p.instock_warn, s.style, i.amount
    FROM shop_product p,  shop_style s, shop_inventory i
    WHERE (i.styleID = s.ID)
      AND (s.productID = p.ID)
    """)
# % zikeshop.siteID
#    AND p.instock_warn <= i.amount
#      AND (p.siteID = %i)


for row in cur.fetchall():
    print row
