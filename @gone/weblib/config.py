"""weblib/config.py - configuration module for weblib

This module stores local configuration options for weblib.
It should define the following variables:

pool : the default SessPool object

"""


import SessPool
from sqlTest import dbc

pool = SessPool.SqlSessPool(dbc)
