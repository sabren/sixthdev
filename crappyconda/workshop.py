
from strongbox import *

def indent(text):
    return "\n".join(["    " + line for line in text.split("\n")])

class ProtoAttr(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    type = attr(str)
    okay = attr(str)
    init = attr(str)
    size = attr(int)

    def asCode(self):
        assert self.name, "attribute must have a name"
        assert self.type, "no type for attribute %s" % self.name
        return "%s = attr(%s)" % (self.name, self.type)


class ProtoLink(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    fieldname = attr(str)
    owner = link(forward("workshop.ProtoClass"))
    type = link(forward("workshop.ProtoClass"))
    join = link(forward("workshop.ProtoJoin"))

    def asCode(self):
        assert self.type, "link %s has no type" % self.name
        return "%s = link(forward('?.%s'))" % (self.name, self.type.name)

class ProtoJoin(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    owner = link(forward("workshop.ProtoClass"))
    type = link(forward("workshop.ProtoClass"))    
    fieldname = attr(str)

    def asCode(self):
        assert self.name, "join must have a name"
        assert self.type, "no type for join %s" % self.name
        return "%s = linkset(forward('?.%s'), None)" \
               % (self.name, self.type.name)


class ProtoClass(Strongbox):
    ID = attr(long)
    name = attr(str)
    note = attr(str)
    tablename = attr(str)
    attrs = linkset(ProtoAttr, None)
    links = linkset(ProtoLink, "owner")
    joins = linkset(ProtoJoin, "owner")

    def asCode(self):
        res = []
        res.append("class %s(Strongbox):" % self.name)
        for each in self.attrs + self.links + self.joins:
            res.append(indent(each.asCode()))
        res.append("    pass")
        return "\n".join(res) + "\n"


class Model:
    def __init__(self):
        self.classes = []
    def add(self, klass):
        self.classes.append(klass)
    def classDefs(self):
        return "\n".join([c.asCode() for c in self.classes])
    def finishForwards(self):
        res = []
        for klass in self.classes:
            for each in klass.links + klass.joins:
                res.append("%s.__attrs__['%s'].type=%s" \
                           % (klass.name, each.name, each.type.name ))
        return "\n".join(res)
                
    def asCode(self):
        res = []
        res.append(self.classDefs())
        res.append(self.finishForwards())
        return "\n".join(res)



class ClassCell(Strongbox):
    ID = attr(long)
    what = link(ProtoClass)
    tablename = attr(str)
class LinkCell(Strongbox):
    ID = attr(long)
    what = link(ProtoLink)
    tablename = attr(str)
    fieldname = attr(str)
class JoinCell(Strongbox):
    ID = attr(long)
    what = link(ProtoJoin)
    tablename = attr(str)
    fieldname = attr(str)

class ProtoMap(Strongbox):
    ID = attr(long)
    ccells = linkset(ClassCell, None)
    lcells = linkset(LinkCell, None)
    jcells = linkset(JoinCell, None)

    def asCode(self):
        res = []
        res.append("{")
        for each in self.ccells:
            res.append(each.what.name + ":" + repr(each.tablename) + ",")
        for each in self.lcells + self.jcells:
            res.append(each.what.owner.name
                       + ('.__attrs__["%s"]' % each.what.name)
                       + ":"
                       + "(" + repr(each.tablename) + ","
                       + repr(each.fieldname) + ")," )
            
        res.append("}")
        return "\n".join(res)


ProtoLink.__attrs__["type"].type = ProtoClass
ProtoLink.__attrs__["owner"].type = ProtoClass
ProtoJoin.__attrs__["type"].type = ProtoClass
ProtoJoin.__attrs__["owner"].type = ProtoClass
ProtoClass.__attrs__["attrs"].type = ProtoAttr
ProtoClass.__attrs__["links"].type = ProtoLink


if __name__=="__main__":

    try:
        OUTFILE = sys.argv[1]
    except:
        print "usage: workshop.py OUTFILE"
        sys.exit()

    out = open(OUTFILE,"w")

    print >> out, "##"
    print >> out, "## GENERATED FILE. DO NOT CHANGE!"
    print >> out, "##"

    print >> out,  "from strongbox import *"
    print >> out,  "from pytypes import *"
    print >> out,  "from sixthday import AdminApp"
    print >> out,  "import workshop"
    print >> out
