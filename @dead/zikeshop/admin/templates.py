
import weblib
weblib.auth.check()

tpls = [
    'address',
    'cart',
    'category',
    'foot',
    'get_bill',
    'get_card',
    'get_ship',
    'head',
    'login',
    'product',
    'receipt',
    'sslfoot',
    'sslhead',
    ]

which = weblib.request.get("which")

import header
print '<p align="center"><form action="templates.py" method="GET">'
print '<b>Choose a template to edit:</b>'
print '<select name="which">'
for tpl in tpls:
    print '<option%s>%s</option>' % ((""," SELECTED")[tpl==which], tpl)
print '</select>'
print '<input type="submit" value="go">'
print '</form></p>'



def tpldir():
    import zikeshop
    if hasattr(zikeshop, "tpldir"):
        return zikeshop.tpldir
    else:
        #@TODO: unhardcode base directory for templates
        return "/usr/home/zike/web/zike/users/%s" \
               % weblib.auth.user.username

if weblib.request.get("action") == "save":

    contents = weblib.request.get("contents") + "\n"

    ## save the template...
    f = open(tpldir() + "/tpl_" + which + ".zbr", "w")
    f.write(contents)
    f.close()

    ## compile the template:
    import zebra
    contents = zebra.Z2X().translate(contents)
    f = open(tpldir() + "/tpl_" + which + ".py", "w")
    f.write(zebra.Bootstrap().compile(contents))
    f.close()
    
elif which:

    contents = weblib.htmlEncode(
        open(tpldir() + "/tpl_" + which + ".zbr").read())


    print '<h3>editing %s</h3>' % which
    print '<form action="templates.py" method="post">'
    print '<table><tr><td>'
    print '<textarea cols="75" rows="15" name="contents">%s</textarea>' \
          % contents
    print '</td></tr><tr><td align="right">'
    print '<input type="hidden" name="which" value="%s">' % which
    print '<input type="submit" name="action" value="save">'
    print '</td></tr></table>'
    print '</form>'
    

