#!/usr/bin/python
"""
<h2>this is not a quickbooks data file</h2>

<p>2004-1-22 11:59:32</p>

<p>A few weeks ago my laptop announced that a possible hard drive
failure was imminent so of course I backed up all my data and sent it
in for repairs. No big deal. But now Quickbooks won't read my old
files. I've regretted buying that piece of crap since day one anyway,
so here, just in case it comes in handy for someone out there someday,
is today's lesson:</p>

<h2>how to convert quickbooks 2001 to quicken 2004</h2>


<p><b>step 1: export the data.</b> To import to quicken we need a
*.qfx file (really OFX, which the banks all use) or a QIF file (which
is the old quicken interchange format, no longer in use). There's no
way to export either of these from quickbooks 2001 even if I could
read the file. Luckily (?) last April I gave a copy of my file to my
accountant. Her QuickBooks automatically upgraded my file, and of
course (according to Intuit's knowledge base) it is completely
impossible to convert it back. They said the only fix was to upgrade
my copy. Instead, I had my accountant dump it to a text file:</p>

<ul>
<li>go to the account you want to export (you may
    have to do this for each account - i only had one)</li>
<li>click "print"</li>
<li>select "from" the first transaction date "to" today</li>
<li>check the "print splits detail" box</li>
<li>click "OK"</li>
<li>select print to: file</li>
<li>select "Tab delimited file"</li>
<li>click "Print"</li>
<li>save the file as whatever.txt</li>
</ul>

<p><b>step 2: transform the data.</b> Here, python is our friend. :)
(more later once I get back from the gym) </p>
"""

# http://www.intuit.com/support/quicken/2003/win/1178.html
# http://www.intuit.com/support/quicken/2003/win/1181.html
import sys
from pytypes import FixedPoint

class Transaction(object):
    def __init__(self):
        self.number = None
        self.split = []
class SplitLine(object):
    pass


try:
    textData = open(sys.argv[1]).read().split("\n")[4:]
except:
    print "usage: txt2qif.py fileName"
    sys.exit()


autoNumber = 0
transactions = []
trans = None
for line in textData:
    if not line.strip(): continue
    if line.startswith("\t"):
        _1, category, memo, payment, _2, deposit  =  line.split("\t")
        assert (_1 == "") and (_2=="")
        split = SplitLine()
        split.category = category
        split.memo = memo
        assert (payment and not deposit) or (deposit and not payment) # xor :(
        split.amount = FixedPoint((payment or deposit).replace(",",""))
        #print "%7s  %-20s %-20s" % (split.amount, split.category, split.memo)
        trans.split.append(split)
    else:
        date, number, payee, account, memo, payment, c, deposit, balance \
              = line.split("\t")
        transactions.append(Transaction())
        trans = transactions[-1]
        trans.date = date

        if number in ["", "d","debit","Debit","s","D","10000","10001"]:
            trans.memo = memo
        else:
            trans.memo = "#%s: %s" % (number, memo)

            
        autoNumber += 1
        trans.number = autoNumber
            
        trans.payee = payee
        trans.category = account


        # cleared flag: 
        if c == "X":
            trans.c = "R"
        elif c =="":
            trans.c = ""
        else:
            raise Exception("unrecognized cleared value: [%s]" % c)

        # amount:
        if deposit:
            trans.amount = FixedPoint(deposit.replace(",",""))
        elif payment:
            trans.amount = FixedPoint(payment.replace(",","")) * -1
        else:
            trans.amount = None
            assert memo.count("VOID")


print "!Type:Bank"
for t in transactions:
    print "%s || %s" % (t.number, t.memo)
    continue
    print "D%s" % t.date
    print "N%s" % t.number
    print "P%s" % t.payee
    print "L%s" % t.category
    print "M%s" % t.memo
    if t.amount is not None: # handle VOIDs
        print "U%s" % t.amount
    print "CR" # status in "cleared column */R etc
    for s in t.split:
        print "S%s" % s.category
        print "E%s" % s.memo
        print "$%s" % s.amount
    print "^"
