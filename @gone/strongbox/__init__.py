"""
$Id$

This package provides observable classes with static typing.
"""
import warnings

class forward:
    """
    dummy class for defining recursive structures)
    does absolutely nothing.
    """
    def __init__(self, typename=None):
        #@TODO: now that initialvalue passes instance,
        #@TODO: make forward('Whatever') take a module.Class
        #@TODO: and do some kind of morphing trick.
        if type(typename) != str:
            warnings.warn("forward() should be forward('module.ClassName')")


from Attribute import Attribute as attr
from Link import Link as link
from LinkSet import LinkSet as linkset

from Private import Private
from BoxMaker import BoxMaker
from MetaBox import MetaBox
from BlackBox import BlackBox
from WhiteBox import WhiteBox
from BoxView import *

# for backwards compatability:
Strongbox = WhiteBox
