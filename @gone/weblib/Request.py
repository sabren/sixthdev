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

import os
import string
import weblib

class Request:
    
    def __init__(self, querystring=None, form=None, environ=None, cookie=None, engine=weblib):

        self.engine = engine

        ## environment
        if environ is None:
            self.environ = os.environ
        else:
            self.environ = environ
        

        ## querystring:
        ## @TODO: handle urlencoding/decoding
        if querystring is not None: # test explicitly. we might want to pass a ""
            self.querystring = querystring
        elif self.environ.has_key("QUERY_STRING"):
            self.querystring = self.environ["QUERY_STRING"]
        else:
            self.querystring = ""

        ## query, a hash of the querystring
        self.query = {}
        for pair in string.split(self.querystring, "&"):
            l = string.split(pair, "=", 1)
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ''
            self.query[k]=v


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


