"""weblib/config.py - configuration module for weblib

This module stores local configuration options for weblib.
It should define the following variables:

pool : the default SessPool object

"""


import SessPool
from sqlTest import dbc

pool = SessPool.SqlSessPool(dbc)


if __name__=="__main__":
    print
    print "edit this module's source to configure your weblib installation."
    print
    
