#@TODO: lazy module loading..
from config import dbc
from Product import Product
from Cart import Cart
from Style import Style

#@TODO: chicken and egg problem! :/ [need a factory?]
Product._links["styles"][1] = Style

from PublicApp import PublicApp
from Category import Category
from Customer import Customer
from FixedPoint import FixedPoint
from CustomerAuth import CustomerAuth
#from Status import Status
from Detail import Detail
from Sale import Sale
from Store import Store
from Card import Card
from State import State
from SaleEditor import SaleEditor

### PICTURE ROUTINE #######################

def showPicture(ID=None, size=None):
    """shows the specified picture.. Should be the only thing called
    on the page."""

    import weblib
    import zikebase, zikeshop
    import Image, cStringIO

    if ID is None:
        ID=weblib.request["ID"]
    if size is None:
        size = int(weblib.request.get("size",0))
        
    picture = zikebase.Picture(ID=ID)
    assert picture.siteID == zikeshop.siteID, \
           "Not your image. (zikeshop.siteID: %i), (image.siteID: %i)" \
           % (zikeshop.siteID, picture.siteID)
    weblib.response.contentType=picture.type
    if size:
        im = Image.open(cStringIO.StringIO(picture.picture))
        im.thumbnail((size,size))
        im.save(weblib.response, im.format)
    else:
        weblib.response.write(picture.picture)
        
        
####### MAIL ROUTINE #######################

def sendmail(fromaddr, toaddr, subj, msg):
    """utility routine to make it easy to send mail.."""
    import os
    mail = os.popen("sendmail %s" % toaddr, "w")
    mail.write("From:%s\nTo: %s\nSubject: %s\n\n%s\n" \
               % (fromaddr, toaddr, subj, msg))
    mail.close()
    
