"""
$Id$

This package provides observable classes with static typing.
"""

class StrongboxError(Exception): pass
class forward: "(dummy class for defining recursive structures)"

from Observable import Observable
from Attribute import Attribute as attr
from Link import Link as link
from LinkSet import LinkSet as linkset
from Stealthbox import *
from Strongbox import *
from BoxView import *
