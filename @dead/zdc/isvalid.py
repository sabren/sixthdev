"""
data validation routines for zdc..
eg, if zdc.isvalid.email('xxx'): ...
"""
__ver__="$Id$"

STATES = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
          'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD',
          'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
          'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
          'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY',]
EXT_STATES = ["DC","GU","PR","VI"] # DC, Guam, Puerto Rico, Virgin Islands

def state(CD, includeNonStates=1):
    """
    state(CD) -> is CD a valid 2 letter US state abbreviation?
    state(CD,0) -> EXcludes US territories and DC
    """
    if includeNonStates:       
        return ((CD in STATES) or (CD in EXT_STATES))
    else:
        return (CD in STATES)


def email(string):
    "email(string) -> is string a valid email address?"
    import re
    pattern = r'^(\w|\d|_|-)+(\.[a-zA-Z0-9_\-]+)*' \
              r'@(\w|\d|_|-)+(\.[a-zA-Z0-9_\-]+)+$'
    return re.match(pattern, string)
    


if __name__=="__main__":
    assert email('sabren@manifestation.com')
    assert email('michal.sabren@manifest-station.com')
    assert not email('laskdjf..asdf@sadf.com')
    assert not email('asdf@@asdf.asc')
    assert not email('aslkdjf')
    assert state('TX')
    assert state('VI')
    assert not state('VI',0)
    assert not state('EE')
