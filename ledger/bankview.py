#!/usr/local/bin/python2.4
import sys
import ledger

#e = re.compile(r"(\d{4}/\d{2}/\d{2})(.*){(\d{4}/\d{2}/\d{2})}")
#
#for line in sys.stdin:
#    sys.stdout.write(e.sub(r"\3\2",line))
    
book = ledger.parseLedger(sys.stdin.read())
book = ledger.bankView(book)

for item in book:
    print item
