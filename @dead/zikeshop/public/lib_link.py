
def link_category(path):
    'return a link to a category.'
    import weblib
    return "shop.py?action=show&what=category&path=%s" \
           % weblib.urlEncode(path)

def link_product(code):
    'return a link to a product.'
    return "shop.py?action=show&what=product&code=%s" % code

def link_picture(ID, size=None):
    'return a link to a picture, optionally thumbnailed'
    if size:
        return "picture.py?ID=%s" % ID
    else:
        return "picture.py?ID=%s&size=%s" % (ID, size)

#@TODO: consolidate all these three:

def link_action(action, params=""):  #@TODO: rename as link_shop (do I even need it?)
    'retun a link back to the cart, given the appropriate action and params'
    if params:
        return "shop.py?action=%s&%s" % (action, params)
    else:
        return "shop.py?action=%s" % action

def link_cart(action="", params=""):
    if action:
        if params:
            return "cart.py?action=%s&%s" % (action, params)
        else:
            return "cart.py?action=%s" % action
    else:
        return "cart.py"


def link_checkout(action="", params=""):
    if action:
        if params:
            return "checkout.py?action=%s&%s" % (action, params)
        else:
            return "checkout.py?action=%s" % action
    else:
        return "checkout.py"

def link_user(action="", params=""):
    if action:
        if params:
            return "user.py?action=%s&%s" % (action, params)
        else:
            return "user.py?action=%s" % action
    else:
        return "user.py"



model = {
    "link_category": link_category,
    "link_product": link_product,
    "link_picture": link_picture,
    "link_action": link_action,
    "link_cart": link_cart,
    "link_checkout": link_checkout,
    "link_user": link_user,
    }
