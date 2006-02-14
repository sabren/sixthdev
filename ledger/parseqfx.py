#!/usr/bin/python
"""
qfx (web connect file) parser 
"""
import sys, re
sys.path.append("/Users/michal/lib")
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



from cashqueue import Transaction
import cash2led

reDes = re.compile("DES=(.*)")
def makeTransaction(date, name, amount):
    t = Transaction()
    t.amount = amount
    t.date = date

    if name.startswith("PAYPAL"):
        if t.amount > 0:
            t.comment = "paypal"
            t.lines.append(("asset:checking", amount))
            t.lines.append(("income:hosting", ))
        else:
            t.comment = "[???] " + name

    elif name.startswith("BOFA MS"):
        if name.count("MERCH SETL"):
            t.comment = "bofa ms"
            t.lines.append(("asset:checking", amount))
            t.lines.append(("asset:merchant", ))
        elif name.count("MERCH FEES"):
            t.comment = "bofa ms fees"
            t.lines.append(("expense:fees:bofams", -amount))
            
    elif name.startswith("OVERDRAFT"):
        t.comment = "overdraft"
        t.lines.append(("expense:fees:overdraft", -amount))

    elif name.startswith("Overdraft Interest"):
        t.comment = "overdraft interest"
        t.lines.append(("expense:fees:overdraft", -amount))
        
    elif name == "AMERICAN EXPRESS;DES=SETTLEMENT;":
        t.comment = "amex"
        # already have data broken down from cashqueue
        
    elif name in ("Deposit", "Counter Credit"):
        t.comment = "checks"
        # should already have data here, too        
        
    elif name.count("DES=ADP - FEES"):
        t.comment = "adp"
        t.lines.append(("expense:fees:adp", -amount))
        
    elif name.count("DES=ADP - TAX"):
        t.comment = "adp"
        t.lines.append(("expense:payroll", -amount))

    elif name.count("Monthly Maintenance Fee"):
        t.comment = "monthly maintenance fee"
        t.lines.append(("expense:fees:bofa", -amount))

    elif name.startswith("CHECKCARD"):
        _, when, memo = name.split(None, 2)
        t.clearedOn = Date(date.toUS()) # make a copy
        t.date.m = int(when[:2])
        t.date.d = int(when[2:])
        t.comment = "[???] %s" % memo

        # and we know two types of check card:
        if memo.count("RACKSPACE"):
            t.comment = "rackspace"
            t.lines.append(("expense:datacenter", -amount))
        elif memo.count("EV1.NET"):
            t.comment = "ev1"
            t.lines.append(("expense:datacenter", -amount))
            
    else:
        t.comment = "[???] " + name


    # fill in default account data:
    if len(t.lines) == 0:
        t.lines.append(("unknown", -amount))
    if len(t.lines) == 1:
        t.lines.append(("asset:checking", ))
    
    return t



def printTransaction(t):
    print cash2led.fmtDate(t.date), t.comment,
    if t.clearedOn:
        print "{%s}" % cash2led.fmtDate(t.clearedOn)
    else:
        print
    for line in t.lines:
        if len(line) == 2:
            print cash2led.fmt % line
        else:
            print cash2led.indent, line[0]
    print





if __name__=="__main__":

    try:
        _, filename = sys.argv
    except:
        print "usage: parseqfx.py filename"
        sys.exit()

    data = parse(open(filename))
    data.rows.reverse()
    for row in data.rows:
        t = makeTransaction(row["date"], row["NAME"], row["amount"])
        printTransaction(t)

    print ";", len(data.credits()), "credits:", data.amtIn()
    print ";", len(data.debits()), "debits:", data.amtOut()
