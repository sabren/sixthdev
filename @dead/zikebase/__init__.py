"""
zikebase: a framework for data-driven websites.

$Id$
"""

from config import dbc

__objs=(
    'Content',
    'Picture',
    'User',
    'UserAuth',
    'ObjectEditor',
    'Node'
    )


## This is an auto-loading function that makes sure classes only get
## loaded the first time we request them. this is handy not only for
## keeping a small footprint, but also because it lets you redefine
## the classes after zikebase has been loaded.. You might want to do
## this, for example, in a .weblib.py ...

for __item in __objs:
    _ = "def %s(*args, **kwargs):"           "\n" \
        "    import zikebase, %s"            "\n" \
        "    zikebase.%s = %s.%s"            "\n" \
        "    return apply(%s.%s, args, kwargs)\n"
    _ = _ % ((__item,) * 7)
    exec(_)

