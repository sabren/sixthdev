"""
this module configures database mapping for rantelope
"""
__ver__="$Id$"
import storage
import arlo
from rantelope import *

## database connection ############################
# ( you could also use MySQLdb and MySQLStorage here )
#import sqlite
#dbc = sqlite.connect("db/blog.rdb")
#sto = storage.PySQLiteStorage(dbc)

import sys; sys.path.append("/home/sabren/lib")
from sqlGuru import dbc
sto = storage.MySQLStorage(dbc)



## object-relational mapping ######################
dbmap = {Channel: "rnt_channel",
         Channel.__attrs__["stories"]: (Story, "channelID"),
         Channel.__attrs__["categories"]: (Category, "channelID"),
         Category: "rnt_category",
         Story: "rnt_story",
         Story.__attrs__["comments"]: (Comment, "storyID"),
         Story.__attrs__["author"]: (Author, "authorID"),
         Comment: "rnt_comment",
         Author: "rnt_author"}
clerk = arlo.CallbackClerk(sto, dbmap)

## search engine stuff ############################
import atexit
from rantelope import StoryIndex
index = StoryIndex(clerk, "db/index.rk")
clerk.onStore(Story, index.addStory)
atexit.register(index.close)
