
import re

class EmailAddress(object):

    regex = r'^(\w|\d|_|-)+(\.[a-zA-Z0-9_\-]+)*' \
            r'@(\w|\d|_|-)+(\.[a-zA-Z0-9_\-]+)+$'
    
    def __init__(self, value):
        if not re.match(self.regex, value):
            raise TypeError, "invalid EmailAddress"
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __cmp__(self, other):
        return cmp(self.value, other)

