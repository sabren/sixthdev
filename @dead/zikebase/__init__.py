"""
zikebase: a framework for data-driven websites.

$Id$

This package uses a just-in-time import mechanism that makes sure
classes only get loaded if we request them. This is handy not only for
keeping a small footprint, but also because it lets you redefine the
classes after zikebase has been loaded.. You might want to do this,
for example, in a .weblib.py ... It should be transparent to the user:

>>> import zikebase
>>> zikebase.Node
<function Node at a3c80>
>>> zikebase.Node()
<zikebase.Node.Node instance at ccd30>


... However, we sometimes want to mess with the class directly before
instantiating it.. Perhaps to mess with the defaults or whatnot.  The
load() function lets us do that. For example:

>>> import zikebase
>>> zikebase.Node
<function Node at a3c80>
>>> zikebase.load("Node")
>>> zikebase.Node
<class zikebase.Node.Node at f3700>

"""

from config import dbc

__objs=(
    'Content',
    'Picture',
    'User',
    'UserAuth',
    'Password',
    'ObjectEditor',
    'Node',
    )

for __item in __objs:
    _ = "def %s(*args, **kwargs):"           "\n" \
        "    import zikebase, %s"            "\n" \
        "    zikebase.%s = %s.%s"            "\n" \
        "    return apply(%s.%s, args, kwargs)\n"
    _ = _ % ((__item,) * 7)
    exec(_)

    
def load(what):
    """Loads a class directly, replacing the JIT loader."""

    exec("import zikebase; from %s import %s; zikebase.%s = %s"
         % ((what,) * 4))

    
