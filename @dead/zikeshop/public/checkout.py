"""
checkout process for the cart (records the sale)

$Id$
"""
import zikeshop
import weblib

weblib.auth.check()

useTax = 0
isSubmitted = 1

cart = zikeshop.Cart()
# I don't think these are actually part of cart..
# I think I added them in to make the PHP3 port easier.
# @TODO: they probably ought to be part of Cashier or something.

if weblib.request.get("shipmeth"):
    cart.shipmeth = weblib.request.get("shipmeth")

if (useTax != ""):
    cart.useTax = useTax

cash = zikeshop.Cashier(cart, weblib.auth.user)
cash.act()

