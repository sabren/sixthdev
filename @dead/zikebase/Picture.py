"""
Picture.py - an object for storing and manipulating web graphics

$Id$
"""

import zikebase
import zdc

class Picture(zdc.RecordObject):
    _table = zdc.Table(zikebase.dbc, "base_picture")
