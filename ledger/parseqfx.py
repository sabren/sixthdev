#!/usr/bin/python
"""
qfx (web connect file) parser 
"""
import sys
from pytypes import Date, FixedPoint


class OfxData(object):
    def __init__(self):
        self.rows = []
        self.this = None

    def startTag(self, tag):
        if tag == "STMTTRN":
            self.this = {}
            self.rows.append(self.this)

    def closeTag(self, tag):
        self.this=None

    def setValue(self, tag, value):
        if self.this is None:
            pass
        elif tag=="DTPOSTED":
            self.this['date']=Date("%s-%s-%s" % (
                value[:4], value[4:6], value[6:8]))
        elif tag=="TRNAMT":
            self.this['amount']=FixedPoint(value)
        else:
            self.this[tag]=value

    def credits(self):
        return [r for r in self.rows if r["amount"] > 0]

    def debits(self):
        return [r for r in self.rows if r["amount"] < 0]

    def amtIn(self):
        return sum([r["amount"] for r in self.credits()])

    def amtOut(self):
        return sum([r["amount"] for r in self.debits()])


def parse(file):
    data = OfxData()
    
    for line in file:
        line = line.strip()
        
        if line.startswith("</"):
            data.closeTag(line[2:-1])
            
        elif line.startswith("<") and line.endswith(">"):
            data.startTag(line[1:-1])
            
        elif line.startswith("<"):
            data.setValue(*line[1:].split(">",1))
                
        else:
            # irrelevant data
            # print line
            pass
            
    return data



if __name__=="__main__":

    try:
        _, filename = sys.argv
    except:
        print "usage: parseqfx.py filename"
        sys.exit()

    

    data = parse(open(filename))
    for row in data.rows:
        print row
    
    print len(data.credits()), "credits:", data.amtIn()
    print len(data.debits()), "debits:", data.amtOut()
