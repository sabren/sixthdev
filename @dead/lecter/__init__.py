"""
lecter - a logical language
"""
__ver__="$Id$"

TRUE =1
FALSE=0

class Reset(Exception):
    pass

## this dancing around is all
## so we can reset the interpreter.
import Interpreter; reload(Interpreter)
from Interpreter import Interpreter

import Shell; reload(Shell)
from Shell import Shell

