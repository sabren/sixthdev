
#@TODO: lazy module loading..
from Picture import Picture
from Contact import Contact
from Product import Product
from Cart import Cart
from Style import Style
from PublicApp import PublicApp
from Category import Category
from Detail import Detail
from Sale import Sale
from SaleEditor import SaleEditor
from Store import Store
from Card import Card
from State import State

### PICTURE ROUTINE #######################

def showPicture(DBC, RES, ID=None, size=0):
    """
    shows the specified picture.. Should be the only thing called
    on the page.
    """
    import Image
    import cStringIO

    assert ID is not None

    picture = Picture(DBC, ID=ID)
    RES.contentType=picture.type
    if size:
        im = Image.open(cStringIO.StringIO(picture.picture))
        im.thumbnail((size,size))
        im.save(RES, im.format)
    else:
        RES.write(picture.picture)
        
        
####### MAIL ROUTINE #######################

def sendmail(fromaddr, toaddr, subj, msg):
    """utility routine to make it easy to send mail.."""
    import os
    mail = os.popen("sendmail %s" % toaddr, "w")
    mail.write("From:%s\nTo: %s\nSubject: %s\n\n%s\n" \
               % (fromaddr, toaddr, subj, msg))
    mail.close()
    
