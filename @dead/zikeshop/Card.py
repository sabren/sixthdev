"""
(credit) Card object for zikeshop
"""
__ver__="$Id$"

import zdc
import zikeshop

class Card(zdc.RecordObject):
    __super = zdc.RecordObject
    _table = zdc.Table(zikeshop.dbc, "shop_card")
    __members__= [
        'masked'
        ]

    def get_masked(self):
        return ("x" * (len(self.number)-4)) + self.number[-4:]


    def checkdigits(self, digits):
        return validate(digits)

    def set_number(self, value):
        if self.checkdigits(value):
            self._data['number']=value
        else:
            raise ValueError, "Invalid credit card number."




##### @TODO: THIS CAME FROM THE PAYMENT MODULE. PUT IT BACK THERE! #######
def validate(number):
    """
    validate the format of a credit card number..
    this is tested extensively against perl's Business::CreditCard
    in the zike payment module (outside zikeshop)

    I'm just sticking this in here for now, until the payment
    library is ready to go..

    If there's a bug, put it right in payment first!!!
    (but i don't think there's any bugs, since I tested it against
    all kinds of card #'s and compared to perl)
    """
    # numbers only:
    try:
        long(number)
    except:
        return 0

    # must be at least 13 digits:
    if len(str(number)) < 13:
        return 0
    
    ### check the digits: ###########
    # see http://www.beachnet.com/~hstiles/cardtype.html

    # digits, from right to left...
    digits = list(str(number))
    digits.reverse()

    doubles = ""
    sum = 0
    # Step 1: Double the value of alternate digits of the primary
    # account number beginning with the second digit from the right
    # (the first right--hand digit is the check digit.)
    for i in range(len(digits)):
        if i % 2:
            # note that this does NOT fire for the rightmost digit,
            # because 0 % 2 is 0... :)
            doubles = doubles + str(int(digits[i]) * 2)

    # Step 2: Add the individual digits comprising the products
    # obtained in Step 1 to each of the unaffected digits in the
    # original number.
        else:
            sum = sum + int(digits[i])

    for ch in doubles:
        sum = sum + int(ch)

    # Step 3: The total obtained in Step 2 must be a number ending in
    # zero (30, 40, 50, etc.) for the account number to be validated.
    if (sum % 10) != 0:
        return 0

    return 1
