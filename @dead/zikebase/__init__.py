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

import zdc
dbc=zdc.Connection()

__objs=(
    'Contact',
    'Content',
    'Picture',
    'User',
    'UserAuth',
    'Password',
    'Rot13Password',
    'ObjectEditor',
    'Node',
    'UserApp',
    'AdminApp',
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
  

def sendmail(mail):
    import os
    sender = os.popen("sendmail -t", "w")
    sender.write(mail)
    sender.close()

def randpass(passlen=5):
    """
    This routine generates a random password.
    """
    import whrandom
    # we'll only use easy to interpret symbols (no 1/l 0/o worries)
    ok = "abdefghijkmnopqrstuvwxyz" + "23456789" + "23456789"
    res = ""
    for i in range(passlen):
        res = res + ok[whrandom.randint(0,len(ok)-1)]
    return res

