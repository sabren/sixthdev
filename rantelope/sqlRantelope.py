"""
this module configures database mapping for rantelope
"""
__ver__="$Id$"
#import sys; sys.path.insert(0,"/home/sabren/lib")
import storage
import clerks
from rantelope import *

## database connection ############################
# ( you could also use MySQLdb and MySQLStorage here )
#import sqlite
#dbc = sqlite.connect("db/blog.rdb")
#sto = storage.PySQLiteStorage(dbc)

from sqlGuru import dbc
sto = storage.MySQLStorage(dbc)

clerk = clerks.CallbackClerk(sto, SCHEMA)

## search engine stuff ############################
import atexit
from rantelope import StoryIndex
##############################
#
# ! ! ! ! WARNING ! ! ! !
#
# be careful before changing this path: the full path
# is currently needed because of onerant.app calling
# this file through importing rantelope on the OTHER
# blogs, eg cashflowblogging.com
#
# @TODO: clean this mess up!
#
#index = StoryIndex(clerk, "/home/sabren/web/withoutane.com/rantelope/db/index.rk")
#clerk.onStore(Story, index.addStory)
#atexit.register(index.close)
