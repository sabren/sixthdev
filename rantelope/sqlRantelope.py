"""
this module configures database mapping for rantelope
"""
__ver__="$Id$"
import storage
import arlo
from schema import *

## database connection ############################
# ( you could also use MySQLdb and MySQLStorage here )
import sqlite
dbc = sqlite.connect("blog.rdb")
sto = storage.PySQLiteStorage(dbc)

## object-relational mapping ######################
dbmap = {Channel: "rnt_channel",
         Channel.__attrs__["stories"]: (Story, "channelID"),
         Channel.__attrs__["categories"]: (Category, "channelID"),
         Category: "rnt_category",
         Story: "rnt_story",
         Story.__attrs__["comments"]: (Comment, "storyID"),
         Comment: "rnt_comment",
         Author: "rnt_author"}
clerk = arlo.Clerk(sto, dbmap)
