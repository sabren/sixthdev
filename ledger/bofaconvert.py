
import re
from decimal import Decimal
from amex import fixdate

# this is called reconcile.py but it doesn't
# reconcile anything yet. so far, it just attempts
# to parse a bofa statement (downloaded in pipe format)
# and generates transactions so I can manually copy
# and paste the missing ones into the real ledger

rules = [
    
    # statement regexp , ledger account, ledger note

    (r"AMERICAN EXPRESS DES:SETTLEMENT",
     "expense:fees:amex|asset:merchant",
     "amex"),

    (r"BOFA MS 1924   DES:MERCH FEES",
     "expense:fees:bofams",
     "bofa ms fees"),

    (r"BOFA MS 1924   DES:MERCH SETL",
     "asset:merchant",
     "bofa ms"),

    (r".*LIQUID WEB",
     "expense:datacenter",
     "liquidweb : dcdhosting"),

    (r"ADP PAYROLL FEES DES:ADP - FEES",
     "expense:fees:adp",
     "adp processing fee"),

    (r"PAYPAL",
     "income:hosting",
     "paypal"),

    (r".*THEPLANET.COM",
     "expense:datacenter",
     "ev1 / the planet"),

    (r".*THE PLANET",
     "expense:datacenter",
     "the planet"),

    #"TMobile*HotSpot"

    (r".*GODADY.COM",
     "expense:domains",
     "godaddy"),

    (r".*SAFARIBOOKS",
     "expense:services",
     "safari"),

    (r".*GOOGLE \*ADWORDS",
     "expense:marketing",
     "google adwords"),

    (r"ADP TX/FINCL SVC DES:ADP - TAX ID:E4D1D",
     "liability:accounts:payable|expense:taxes:payroll",
     "adp withholding"),

    (r"ADP TX/FINCL SVC DES:ADP - TAX ID:[^E]",
      "liability:accounts:payable",
      "adp payroll : michal wallace"),

    (r"Monthly Maintenance Fee",
      "expense:fees:bofa",
      "monthly maintenance fee"),
]
rules = [(re.compile(ex), acct, note) for ex,acct,note in rules]


def all_lines(filenames):
    for f in filenames:
        for line in open(f):
            yield line

import sys
if len(sys.argv) > 1:
    stream = all_lines(sys.argv[1:])
else:
    stream = sys.stdin

for line in stream:
    line = line.strip()
    if not line: continue
    fields = line.replace('"','').strip().split("|")
    
    if fields[0][0].isdigit() and not fields[1].startswith("Beginning"):

        date, desc, amount, runBal = fields
        date = fixdate(date)
        amount = Decimal(amount)

        for rule, account, note in rules:
            if rule.match(desc):
                print date, note
                if amount < 0:
                    print "     %-30s  %15s" % ( account, -amount)
                    print "     asset:checking"
                else:
                    print "     asset:checking %32s" % amount
                    print "     %s" % account
                break
        else: # no break in for
            print ';', date, desc
            print ';', "     %-30s  %15s" % ('asset:checking', -amount)
            print ';', '     ???'
            
        print "; balance: %s" % runBal
        print

