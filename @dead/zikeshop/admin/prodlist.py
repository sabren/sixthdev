import zikeshop
import weblib

import header

cur = zikeshop.dbc.cursor()
cur.execute("select * from shop_product where siteID=%i" % weblib.auth.user.siteID) 


print '<table border="1">'

print '<tr>'
for field in cur.description:
    print '<th>%s</th>' % field[0]
print '</tr>'

for row in cur.fetchall():
    print '<tr>'
    for field in row:
        print '<td><a href="e_product.py?ID=%i">%s</a></td>' % (row[0], field)
    print '</tr>'

print '</table>'
