"""
Request.py - emulates the ASP Request object for python CGI's

don't want to use cgi because it has no cookies, and form/querystring
get lumped together. Plus it's old and crufty. :) .. but it also
*works*, so for now we'll use cgi.py after all..

@TODO: license
"""

# @TODO: cookie support
# @TODO: request["x"] should look at all 3 sources
# @TODO: figure out how to treat file uploads


class Request:
    def __init__(self):
        import os, string
        self.environ = os.environ

        ## querystring:
        ## @TODO: handle urlencoding/decoding
        self.querystring = {}
        for pair in string.split(os.environ["QUERY_STRING"], "&"):
            l = string.split(pair, "=", 1)
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ''
            self.querystring[k]=v


        ## cookie:
        ## @TODO: get some real cookie parsing abilities...
        self.cookie = {}
        try:
            for pair in string.split(os.environ["HTTP_COOKIE"], "; "):
                l = string.split(pair, "=", 1)
                k = l[0]
                if len(l) > 1:
                    v = l[1]
                else:
                    v = ''
                self.cookie[k] = v
        except:
            pass # no cookies

        ## form:
        ## @TODO: genericize this split stuff..
        ## @TODO: handle FILE uploads/multipart encoding
        self.form = {}
        try:
            contentLength = int(os.environ["CONTENT_LENGTH"])
            import sys
            content = sys.stdin.read(contentLength)
            for pair in string.split(content, "&"):
                l = string.split(pair, "=", 1)
                k = l[0]
                if len(l) > 1:
                    v = l[1]
                else:
                    v = ''
                self.form[k]=v
        except:
            pass



################## OLD STUFF (NO LONGER IN USE) ####################

#import cgi, Cookie, os

class oldRequest:
    def __init__(self):
        self.environ = os.environ
        self.cookie = Cookie.SmartCookie()
        if os.environ.has_key("HTTP_COOKIE"):
            self.cookie.load(os.environ["HTTP_COOKIE"])

        # @TODO: seperate form/querystring
        self.form = \
        self.querystring = \
        self._dict = cgi.FieldStorage()
        
        def __getitem__(self, key):
            return self._dict[key]

