"""
Request.py - emulates the ASP Request object for python CGI's

$Id$

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


def tupleMerge(head, tail):
    """tupleMerge(head, tail)
    converts head and tail into tuples (if they're not) and merges them"""

    if type(head) != type(()):
        head = (head,)

    if type(tail) != type(()):
        tail = (tail,)

    return head + tail


class Request:
    
    def __init__(self, querystring=None, form=None, environ=None,
                 cookie=None, engine=weblib, content=None):

        self.engine = engine
        if self.engine is weblib:
            weblib.request = self

        ## environment
        if environ is None:
            self.environ = os.environ
        else:
            self.environ = environ
        

        ## querystring:
        ## @TODO: handle urlencoding/decoding
        if querystring is not None:
            self.querystring = querystring
        elif self.environ.has_key("QUERY_STRING"):
            self.querystring = self.environ["QUERY_STRING"]
        else:
            self.querystring = ""

        ## query, a hash of the querystring
        self.query = {}
        for pair in string.split(weblib.urlDecode(self.querystring), "&"):
            l = string.split(pair, "=", 1)
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ''
            if self.query.has_key(k):
                self.query[k] = tupleMerge(self.query[k], v)
            else:
                self.query[k]=v


        ## cookie:
        ## @TODO: get some real cookie parsing abilities...
        self.cookie = cookie
        if cookie is None:
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
        self.form = form
        if not form:
            self.form = {}
            try:
                if content is None:
                    contentLength = int(os.environ["CONTENT_LENGTH"])
                    import sys
                    self.content = sys.stdin.read(contentLength)
                else:
                    self.content = content
                for pair in string.split(weblib.urlDecode(self.content), "&"):
                    l = string.split(pair, "=", 1)
                    k = l[0]
                    if len(l) > 1:
                        v = l[1]
                    else:
                        v = ''
                    self.form[k]=v
            except:
                pass


    ## Dictionary Methods @TODO: more of them ##########################


    def __getitem__(self, key):

        res = None

        for dict in [self.query, self.form, self.cookie, self.environ]:
            if dict.has_key(key):
                if res is None:
                    res = dict[key]
                else:
                    res = tupleMerge(res, dict[key])

        if res is None:
            raise KeyError, key

        return res



    def get(self, key, failobj=None):
        
        try:
            return self[key]
        except KeyError:
            return failobj


    def has_key(self, key):
        if self.get(key):
            return 1
        else:
            return 0
            
            
