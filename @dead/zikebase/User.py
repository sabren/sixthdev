"""
User.py - user object for zikebase

$Id$
"""

import zikebase
import zdc

class User(zdc.RecordObject):
    _table = zdc.Table(zikebase.dbc, "base_user")
