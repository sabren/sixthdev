
import weblib
import zikeshop
import tpl_cart
from zikeshop import dbc

bagger = zikeshop.Bagger(zikeshop.Cart())
bagger.act()


model={"contents":bagger.cart.q_contents(),
       #@TODO: get rid of zikeshop..checkouturl..??
       "checkouturl": weblib.sess.url(getattr(zikeshop, "checkouturl",
                                              "checkout.py")),
       "basehref":zikeshop.basehref}
tpl_cart.show(model)

