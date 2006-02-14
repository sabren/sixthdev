#!/usr/bin/python
"""
qif parser

based on :
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/306103
"""
from pytypes import Date
import cash2led
import sys
 
class QifItem:
    def __init__(self):
        self.order = ['date', 'amount', 'cleared', 'num', 'payee', 'memo', 'address', 'category', 'categoryInSplit', 'memoInSplit', 'amountOfSplit']
        self.date = None
        self.amount = None
        self.cleared = None
        self.num = None
        self.payee = None
        self.memo = None
        self.address = None
        self.category = None
        self.categoryInSplit = None
        self.memoInSplit = None
        self.amountOfSplit = None

    def show(self):
        pass
    
    def __repr__(self):
        titles = ','.join(self.order)
        tmpstring = ','.join( [str(self.__dict__[field]) for field in self.order] )
        tmpstring = tmpstring.replace('None', '')
        return titles + "," + tmpstring

    def dataString(self):
        """
        Returns the data of this QIF without a header row
        """
        tmpstring = ','.join( [str(self.__dict__[field]) for field in self.order] )
        tmpstring = tmpstring.replace('None', '')
        return tmpstring
    
def parseQif(infile):
    """
    Parse a qif file and return a list of entries.
    infile should be open file-like object (supporting readline() ).
    """

    inItem = False

    items = []
    curItem = QifItem()
    line = infile.readline()
    while line != '':
        if line[0] == '\n': # blank line
            pass
        elif line[0] == '^': # end of item
            # save the item
            items.append(curItem)
            curItem = QifItem()
        elif line[0] == 'D':
            curItem.date = cash2led.fmtDate(Date(
                line[1:-1].replace("' ","/200").replace(" ","")))
        elif line[0] == 'T':
            curItem.amount = line[1:-1]
        elif line[0] == "U":
            pass # same as T
        elif line[0] == "N":
            curItem.num = line[1:-1]
        elif line[0] == 'C':
            curItem.cleared = line[1:-1]
        elif line[0] == 'P':
            curItem.payee = line[1:-1]
        elif line[0] == 'M':
            curItem.memo = line[1:-1]
        elif line[0] == 'A':
            curItem.address = line[1:-1]
        elif line[0] == 'L':
            curItem.category = line[1:-1]
        elif line[0] == 'S':
            try:
                curItem.categoryInSplit.append(";" + line[1:-1])
            except AttributeError:
                curItem.categoryInSplit = line[1:-1]
        elif line[0] == 'E':
            try:
                curItem.memoInSplit.append(";" + line[1:-1])
            except AttributeError:
                curItem.memoInSplit = line[1:-1]
        elif line[0] == '$':
            try:
                curItem.amountInSplit.append(";" + line[1:-1])
            except AttributeError:
                curItem.amountInSplit = line[1:-1]
        else:
            # don't recognise this line; ignore it
            print >> sys.stderr, "Skipping unknown line:\n", line

        line = infile.readline()
    return items

if __name__ == "__main__":
    # read from stdin and write CSV to stdout
    items = parseQif(sys.stdin)
    print repr(items[0])
    for item in items[1:]:
        print item.dataString()
