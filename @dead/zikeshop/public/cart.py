
import weblib
import zikeshop
import tpl_cart
from zikeshop import dbc

bagger = zikeshop.Bagger(zikeshop.Cart())
bagger.act()

model={"contents":bagger.cart.q_contents(),
       "basehref":zikeshop.basehref}
tpl_cart.show(model)

