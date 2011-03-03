
#!/usr/bin/python2.5
"""
Log into https://www.americanexpress.com/merchant/

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
import csv

# import pdb; pdb.set_trace()

def cleanup(x):
    # strip out commas and dollar signs in the numbers
    return x.replace(',','').replace("$","")

def fixdate(d):
    m,d,y = d.split("/")
    return "/".join([y,m,d])


def parseline(line):
    """
    cant use csv because not all lines in
    the 
    """


if __name__=="__main__":

    stream = sys.stdin if len(sys.argv)==1 else open(sys.argv[1])
    reader = csv.reader(stream)

    firstTotal = True

    for line in reader:

        if not line: continue

        if line[0] == "Payee Location:":
            real_date = fixdate(line[-1])

        elif line[0] == '4100320225':
            init_date = fixdate(line[2])
            print("%s=%s amex" % ( init_date, real_date))

        elif line[0] == "Totals":

            # the first one is a summary. skip it.
            if firstTotal:
                firstTotal = False
                continue
            
            whatIgot=cleanup(line[-1])
            whatTheyTook=cleanup(line[-3])
            whatWeStartedWith=cleanup(line[-5])

            print("    asset:checking %33s" % whatIgot)
            print("    expense:fees:amex %30s" % whatTheyTook)
            print("    asset:merchant %33s" % -decimal.Decimal(whatWeStartedWith))

