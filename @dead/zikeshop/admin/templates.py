"""
template system (zebra) administrator for zikeshop
"""
__ver__="$Id$"

import weblib
import zebra

tpls = [
    'dsp_cart',
    'dsp_category',
    'dsp_foot',
    'dsp_head',
    'dsp_product',
    'dsp_receipt',
    'frm_billing',
    'frm_card',
    'frm_contact',
    'frm_shipping',
    'frm_signup',
    'ssl_foot',
    'ssl_head',
    ]

which = weblib.request.get("which")

zebra.show("dsp_head")
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
    f = open(tpldir() + "/" + which + ".zb", "w")
    f.write(contents)
    f.close()

    ## compile the template:
    import zebra
    contents = zebra.Z2X().translate(contents)
    f = open(tpldir() + "/" + which + ".py", "w")
    f.write(zebra.Bootstrap().compile(contents))
    f.close()
    
elif which:

    contents = weblib.htmlEncode(
        open(tpldir() + "/" + which + ".zb").read())


    print '<h3>editing %s</h3>' % which
    print '<form action="templates.py" method="post">'
    print '<table><tr><td>'
    print '<textarea cols="70" rows="15" name="contents">%s</textarea>' \
          % contents
    print '</td></tr><tr><td align="right">'
    print '<input type="hidden" name="which" value="%s">' % which
    print '<input type="submit" name="action" value="save">'
    print '</td></tr></table>'
    print '</form>'
    
zebra.show("dsp_foot")