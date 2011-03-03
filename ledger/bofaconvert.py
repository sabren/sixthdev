#!/bin/env python3.0
import re
import sys
from decimal import Decimal
from amex import fixdate

# this attempts to parse a bofa statement (downloaded in pipe format)
# and converts it to a ledger file for reconcilliation.

# @TODO: pipe format is only available for corporate accounts

rule_list = [
        
    # corporate
    # -----------------------------------------------
    # statement regexp , ledger account, ledger note

    (r"2Checkout.com",
     "income:hosting",
     "2co"),

    (r".*(Deposit|DEPOSIT)",
     "income:hosting",
     "checks"),

    (r"AMERICAN EXPRESS DES:SETTLEMENT",
     "expense:fees:amex|asset:merchant",
     "amex"),

    (r"BOFA MS 1924 DES:MERCH FEES",
     "expense:fees:bofams",
     "bofa ms fees"),

    (r"BOFA MS 1924 DES:MERCH SETL",
     "asset:merchant",
     "bofa ms"),

    (r"Payroll Service DES:Fee",
     "expense:fees:payroll",
     "bofa payroll management"),

    (r"ONLINE BUSINESS SUITE ACCT MGMT SERVICES",
     "expense:fees:payroll",
     "acct management"),

    (r".*BORDERS",
     "expense:books",
     "borders"),

    (r".*Kindle",
     "expense:books",
     "kindle store"),

    (r".*LIQUID WEB",
     "expense:datacenter",
     "liquidweb : dcdhosting"),

    (r"ADP PAYROLL FEES DES:ADP - FEES",
     "expense:fees:adp",
     "adp processing fee"),

    (r".*ODESK",
     "expense:contractors:odesk",
     "odesk"),

    (r"Online Banking transfer to CHK 7786",
     "liability:wages:michal",
     "Michal Wallace"),

    (r"OVERDRAFT ITEM FEE",
     "expense:fees:overdraft",
     "overdraft fee"),

    (r"PAYPAL",
     "income:hosting",
     "paypal"),

    (r".*THEPLANET.COM",
     "expense:datacenter",
     "ev1 / the planet"),

    (r".*THE PLANET",
     "expense:datacenter",
     "the planet"),

    (r".*SOFT LAYER",
     "expense:datacenter",
     "softlayer"),

    (r".*APPS4RENT",
     "expense:datacenter",
     "apps4rent"),

    (r".*GODADDY.COM",
     "expense:domains",
     "godaddy"),

    (r".*SAFARIBOOKS",
     "expense:services",
     "safari"),

    (r".*GOOGLE.*ADW",
     "expense:marketing",
     "google adwords"),

    (r"ADP TX/FINCL SVC DES:ADP - TAX ID:E4D1D",
     "liability:wages|expense:taxes:payroll",
     "adp withholding"),

    (r"ADP TX/FINCL SVC DES:ADP - TAX ID:[^E]",
      "liability:wages",
      "adp payroll : michal wallace"),

    (r"Monthly Maintenance Fee",
      "expense:fees:bofa",
      "monthly maintenance fee"),

]


def all_lines(filenames):
    for f in filenames:
        for line in open(f):
            yield line


def main(rule_list):
    rules = []
    last = "(start of file)"
    try:
        for ex,acct,note in rule_list:
            last = ex
            rules.append((re.compile(ex, re.IGNORECASE), acct, note))
    except ValueError as e:
        sys.stderr.write("error parsing the rule list: %s\n" % e)
        sys.stderr.write("last valid rule was:\n")
        sys.stderr.write("%s\n" % last)
        sys.exit()

        
    if len(sys.argv) > 1:
        stream = all_lines(sys.argv[1:])
    else:
        stream = sys.stdin

    for line in stream:
        line = line.strip()
        if not line: continue
        fields = line.replace('"','').strip().split("|")

        if fields[0][0].isdigit():

            if fields[1].startswith("Beginning"):
                print(';; %s\n' % ' '.join(map(str, fields)))
                continue

            date, desc, amount, runBal = fields
            date = fixdate(date)
            amount = Decimal(amount)

            for rule, account, note in rules:
                if rule.match(desc):
                    print(date, note)
                    if amount < 0:
                        print("    %-30s  %16s" % ( account, -amount))
                        print("    asset:checking")
                    else:
                        print("    asset:checking %33s" % amount)
                        print("    %s" % account)
                    break
            else: # no rule matched inside the for loop.
                print(';', date, desc)
                print(';', "    %-30s  %16s" % ('asset:checking', -amount))
                print(';', '    ???')

            print()
            print("; balance: %s" % runBal)
            print()

if __name__ == '__main__':
    main(rule_list)

