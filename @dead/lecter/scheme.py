# shcheme primitives
schem = f = {}

atomP = lambda x: type(x)==type("abc")
listP = lambda x: type(x)==type([])
head  = lambda x: x[0]
tail  = lambda x: (x[1:], None)[len(x)==0]
cons  = lambda h, t: [h] + t
nullP = lambda x: x == []
eqP   = lambda a, b: a == b

