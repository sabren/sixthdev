"""
Goals to be achieved.
"""
__ver__="$Id$"

import zdc
import zikebase
zikebase.load("Node")
class Goal(zikebase.Node):
    __super = zikebase.Node
    _table = zdc.Table(zikebase.dbc, "plan_goal")

    # @TODO: should goals also have target and create dates? I think so.
