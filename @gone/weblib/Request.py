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

import string
import weblib


class Request:

    ## constructor ###################################################
    
    def __init__(self, querystring=None, form=None, environ=None, method=None,
                 cookie=None, engine=weblib, content=None, contentType=None):

        self.engine = engine
        if self.engine is weblib:
            weblib.request = self  # do I still need this?

        ## environment
        self.environ = environ
        if environ is None:
            ## os.environ.copy() actually shares
            ## data with os.environ .. I suppose
            ## because it's an object.. Anyway,
            ## that's bad for us because it makes environ
            ## global, and that's NOT what we want. so
            ## we do the following instead:
            import os
            self.environ = {}
            for item in os.environ.keys():
                self.environ[item] = os.environ[item]
            del os
        del environ
        

        ## querystring:
        self.querystring = querystring
        if querystring is None:
            self.querystring = self.environ.get("QUERY_STRING", "")
        del querystring
        

        ## query, a hash of the querystring:
        self.query = self.parse(self.querystring, decode=1)


        ## cookie:
        ## @TODO: get some real cookie parsing abilities...
        self.cookie = cookie
        if cookie is None:
            self.cookie = self.parse(self.environ.get("HTTP_COOKIE", ""),
                                     splitter=";")
        del cookie
        

        ## content & contentLength:
        self.content = content
        if content is None:
            self.contentLength = int(self.environ.get("CONTENT_LENGTH", 0)) \
                                 or None
            if self.contentLength is not None:
                import sys
                self.content = sys.stdin.read(self.contentLength)
        else:
            self.contentLength = len(content)
        del content


        ## contentType:
        self.contentType = contentType
        if (self.content is not None) and (contentType is None):
            self.contentType=self.environ.get("CONTENT_TYPE")
            if self.contentType is None:
                self.contentType = "application/x-www-form-urlencoded"
                
        self.environ["CONTENT_TYPE"] = self.contentType
        del contentType

            
        ## method
        self.method = method
        if method is None:
            self.method = self.environ.get("REQUEST_METHOD")
            if self.method is None: # still
                if self.content:
                    self.method = "POST"
                else:
                    self.method = "GET"
                self.environ["REQUEST_METHOD"] = self.method
        del method
        

        ## form:
        self.form = form
        if form is None:
            if self.contentType == "application/x-www-form-urlencoded":
                self.form = self.parse(self.content, decode=1)
            else:
                self.form = {}
        del form


        ## multipart/form-data (file upload forms):
        ## @TODO: lots of stuff! probably best to just rewrite this
        ## rather than try to yank stuff out of FieldStorage..

        if (self.content) and (self.contentType[:10]=='multipart/'):

            import cgi, StringIO

            # pretend we're a file (FieldStorage requires this)
            # on the web, this would usually be stdin, which IS a file,
            # but if we assume that, we can't assign to content..
            # perhaps content should be a file-like pointer anyway?
            
            storage = cgi.FieldStorage(StringIO.StringIO(self.content),
                                       environ=self.environ)
            
            for field in storage.keys():                
                ## handle multiple values for one field:
                if type(storage[field]) == type([]):
                    self.form[field] = ()
                    for item in storage[field]:
                        if item.filename:
                            self.form[field]=\
                                self._tupleMerge(self.form[field], item)
                        else:
                            self.form[field]=\
                                self._tupleMerge(self.form[field], item.value)
                ## or a single value for the field:
                elif storage[field].filename:
                    self.form[field]=storage[field]
                else:
                    self.form[field]=storage[field].value
                    
            del storage


    ## private methods #################################################

    def _tupleMerge(self, head, tail):
        """converts head and tail into tuples (if they're not) and merges them"""

        if type(head) != type(()):
            head = (head,)
        if type(tail) != type(()):
            tail = (tail,)
        return head + tail


    def parse(self, what, splitter="&", decode=0):
        res = {}
        for pair in string.split(what, "&"):
            if decode:
                pair = weblib.urlDecode(pair)
            l = string.split(pair, "=", 1)
            k = l[0]
            if len(l) > 1:
                v = l[1]
            else:
                v = ''
            if res.has_key(k):
                res[k] = self._tupleMerge(res[k], v)
            else:
                res[k]=v
        return res



    ## Dictionary Methods @TODO: more of them ##########################


    def __getitem__(self, key):
        res = None
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                if res is None:
                    res = dict[key]
                else:
                    res = self._tupleMerge(res, dict[key])
        if res is None:
            raise KeyError, key
        return res


    def __delitem__(self, key):
        res = None
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                res = 1
                del dict[key]
        if res is None:
            raise KeyError, key

    def get(self, key, failobj=None):
        try:
            return self[key]
        except KeyError:
            return failobj


    def keys(self):
        res = {}
        for dict in [self.query, self.form, self.cookie]:
            for key in dict.keys():
                res[key] = 1
                
        return res.keys()


    def has_key(self, key):
        for dict in [self.query, self.form, self.cookie]:
            if dict.has_key(key):
                return 1
        return 0

