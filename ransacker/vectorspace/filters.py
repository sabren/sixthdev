

class Filter:
    def filter(self,s):
        return s


class CapFilter(Filter):
    def filter(self,s):
        return s.upper()

class StripPunctuationFilter(Filter):
    def filter(self,s):
        return "".join([c for c in s if c in "ABCEDFGHIJKLMNOPQRSTUVWXYZ"])


class CompositeFilter(Filter):
    def __init__(self):
        self.filters = []
    def addFilter(self, f):
        self.filters.append(f)
    def filter(self, s):
        res = s
        for f in self.filters:
            res = f.filter(res)
        return res

class ReverseFilter(Filter):
    def filter(self,s):
        res = [ch for ch in s]
        res.reverse()
        return "".join(res)
        


text = "(@h#)(*e@*l$ltj@$o#%w@$o%r@l%d"
c = CompositeFilter()
print c.filter(text)
c.addFilter(CapFilter())
print c.filter(text)
c.addFilter(StripPunctuationFilter())
print c.filter(text)

c2 = CompositeFilter()
c2.addFilter(c)
c2.addFilter(ReverseFilter())
print c2.filter(text)

c3 = CompositeFilter()
c3.addFilter(ReverseFilter())
c3.addFilter(CapFilter())
print c3.filter(text)

        
