# trailblazer project plan

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
#** how to model narratives?
#*** refactoring language / narrative style
#*** nouns are user supplied: trailblazing (or espionage)
#**** Solution
#***** stick with small objects / composition
#*** verbs: patchwork (extend, delete, patch)
#**** Solution.extend
#*** want to give big picture and fill details in later
#**** blaze(name)
#***** maps name to a position on the list
#***** could just insert to the list but then it screws up our keys
#***** so: placeholder() -> Solution()
#*** want to extend without screwing up the blazes
#**** how to find a point again?
#***** could use trail[x][y][z] but this is ugly
#***** so, recursive trail.follow("x.y.z")
#***** make split char a class member
#**** how to extend the point?
#***** this already works
#**** how to replace the point?
#***** just replace the Solution
#**** how to remove the point?
#***** this would screw up the order, so just set to ""
#*** solution compiler
#**** lost ability to iterate when we went nested
#**** but easy to fix: __iter__

#* saxophone
#** dispatch class (Saxophone)
#*** byDefault(thunk)
#*** onTag(tag, thunk)
#*** parse(file)
#*** parse_string(s)
#** tag handlers
#*** __init__(**args)
#*** onText()
#*** onChild()
#*** onWhitespace()
#*** onEnd() -> result
#** passthrough tag handler
#*** collect text, whitespace, child as string
#*** just rebuild tag onEnd()

#* blazehound solution compiler
#** import saxophone
#** trail:blaze
#** trail:extend
#** trail:patch

#* custom blazefile
#** compare to ant/make
#** give example file
#** how to edit? nxml + multi-mode

