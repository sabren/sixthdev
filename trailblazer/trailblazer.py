# trailblazer: a narrative programming tool
from __future__ import generators

#* trailblazer
#** background: why narratives?
#*** conceptual gap between design and plan
#**** designs evolve over time
#**** intermediate transitions are lost
#*** problem space vs solution space
#**** many problems, many solutions
#**** take problems one at a time
#***** why force developers to reserialze the solution space?
#***** easier to solve in certain orders
#**** build the solution up as we go
#*** transitions are good for people
#**** transitions good for planning
#***** YAGNI vs WDNIY
#***** compare to big design up front
#***** maps clearly to requirements
#**** and good for teaching
#***** docs are just a byproduct
#***** but can be refined later
#***** this idea takes a swing at brooke's law
#*** but computer needs the final solution
#*** how do you serialize that design?
#**** two trails: one for person, one for computer
#**** and make the computer do the work!
#**** simpe example: atexit
# we want this to run, but not until the very end.
# but the computer can remember for us.

#** how to model narratives?
#*** refactoring language / narrative style
#*** nouns are user supplied: trailblazing (or espionage)
#*** verbs: patchwork (extend, delete, patch)

#* custom blazefile
#** compare to ant/make
#** give example file
#** how to edit? nxml + multi-mode

