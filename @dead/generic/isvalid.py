"""
isvalid module... eg.. if isvalid.email('xxx')
"""

def email(string):
    import re
    pattern = r'^(\w|\d|_)+(\.[a-zA-Z0-9_]+)*@(\w|\d|_)+(\.[a-zA-Z0-9_]+)+$'
    return re.match(pattern, string)
    


if __name__=="__main__":
    assert email('sabren@manifestation.com')
    assert email('michal.sabren@manifestation.com')
    assert not email('laskdjf..asdf@sadf.com')
    assert not email('asdf@@asdf.asc')
    assert not email('aslkdjf')
