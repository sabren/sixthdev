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
from pytypes import FixedPoint

class Transaction(object):
    pass
class SplitLine(object):
    pass


transactions = []
trans = None
for line in open("seibofa.txt").read().split("\n")[4:]:
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
    else:
        date, number, payee, account, memo, payment, c, deposit, balance = line.split("\t")
        transactions.append(Transaction())
        trans = transactions[-1]
        trans.date = date
        trans.number = number
        trans.payee = payee
        trans.category = account
        trans.memo = memo

        if account == "-split-":
            trans.split = []

        # cleared flag: 
        if c == "X":
            trans.c = "R"
        elif c =="":
            trans.c = ""
        else:
            raise Exception("don't know how to handle cleared value of [%s]" % c)

        # amount:
        if deposit:
            trans.amount = FixedPoint(deposit.replace(",",""))
        elif payment:
            trans.amount = FixedPoint(payment.replace(",","")) * -1
        else:
            trans.amount = None
            assert memo.count("VOID")


out = open("seibofa.qif","w")
print >> out, "!Type:Bank"
for t in transactions:
    print >> out, "D%s" % t.date
    print >> out, "N%s" % t.number
    print >> out, "P%s" % t.payee
    print >> out, "L%s" % t.category
    print >> out, "M%s" % t.memo
    if t.amount is not None: # handle VOIDs
        print >> out, "U%s" % t.amount
    print >> out, "CR" # status in "cleared column */R etc
    if hasattr(t, "split"):
        for s in t.split:
            print >> out, "S%s" % s.category
            print >> out, "E%s" % s.memo
            print >> out, "$%s" % s.amount
    print >> out, "^"
