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

import cgi, Cookie, os

class Request:
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

request = Request()

