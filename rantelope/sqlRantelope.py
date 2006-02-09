"""
this module configures database mapping for rantelope
"""
__ver__="$Id$"
#import sys; sys.path.insert(0,"/home/sabren/lib")
import storage
import clerks as arlo
from rantelope import *

## database connection ############################
# ( you could also use MySQLdb and MySQLStorage here )
#import sqlite
#dbc = sqlite.connect("db/blog.rdb")
#sto = storage.PySQLiteStorage(dbc)

from sqlGuru import dbc
sto = storage.MySQLStorage(dbc)

clerk = arlo.CallbackClerk(sto, SCHEMA)

## search engine stuff ############################
import atexit
from rantelope import StoryIndex
index = StoryIndex(clerk, "db/index.rk")
clerk.onStore(Story, index.addStory)
atexit.register(index.close)
