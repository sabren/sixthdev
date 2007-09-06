#!/usr/bin/python2.5
"""
Log into americanexpress.com/merchant/

click view your statement
change date range if you want
leave other settings to the defaults

click download
csv
saves as MFAS.csv

copy to p:/bankdata


now run:
   dos2unix MFAS.csv
   python amex.py MFAS.csv > mfas.led

and copy/paste the transactions into the ledger.

"""

import decimal
import sys


# import pdb; pdb.set_trace()

def unquote(x):
    return x.replace('"','').replace("$","")

def fixdate(d):
    m,d,y = d.split("/")
    return "/".join([y,m,d])



if __name__=="__main__":

    stream = sys.stdin if len(sys.argv)==1 else open(sys.argv[1])

    for line in stream.read().split("\n"):

        if line.startswith("Payee Location"):
            real_date = fixdate(line.split(",")[-1])

        if line.startswith('"4100320225"'):
            data = line.split(",")
            init_date = fixdate(unquote(data[2]))

            print "%s=%s amex" % ( init_date, real_date)

        if line.startswith("Totals"):
            data = line.split(",")
            whatIgot=unquote(data[-1])
            whatTheyTook=unquote(data[-3])
            whatWeStartedWith=unquote(data[-5])

            print "    asset:checking %33s" % whatIgot
            print "    expense:fees:amex %30s" % whatTheyTook
            print "    asset:merchant %33s" % -decimal.Decimal(whatWeStartedWith)

