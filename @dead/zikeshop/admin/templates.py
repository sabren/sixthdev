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
print '<form action="templates.py" method="GET">'
print 'Choose a template to edit:'
print '<select name="which">'
for tpl in tpls:
    print '<option%s>%s</option>' % ((""," SELECTED")[tpl==which], tpl)
print '</select>'
print '<input type="submit" value="go">'
print '</form>'

def tpldir():
    import zikeshop
    if hasattr(zikeshop, "tpldir"):
        return zikeshop.tpldir
    else:
        raise hell
        #@TODO: unhardcode base directory for templates

if weblib.request.get("action") == "save":
    contents = weblib.request.get("contents")

    ## save the template...
    f = open(tpldir() + "/" + which + ".zb",
             "wb") # binary more so as not to add extra ^M's on win32
    f.write(contents)
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
