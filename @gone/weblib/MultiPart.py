# multipart crap:

    def _doContentJunk(self, content, form):
        if self.contentType[:10]=="multipart/":
            self._parseMultiPartForm(content)
        else:
            contentLength = int(self.environ.get("CONTENT_LENGTH", 0))
            if contentLength:
                content = sys.stdin.read(contentLength)


    def _parseMultiPartForm(self, stream):
        ## multipart/form-data (file upload forms):
        ## @TODO: lots of stuff! probably best to just rewrite this
        ## rather than try to yank stuff out of FieldStorage..
        form = {}
        import cgi, StringIO

        # pretend we're a file (FieldStorage requires this)
        # on the web, this would usually be stdin, which IS a file,
        # but if we assume that, we can't assign to content..
        # perhaps content should be a file-like pointer anyway?

        if type(stream)==type(""):
            storage = cgi.FieldStorage(StringIO.StringIO(stream),
                                       environ=self.environ)
            #@TODO: this isn't working in test!
        else:
            storage = cgi.FieldStorage(stream, environ=self.environ)

        for field in storage.keys():                
            ## handle multiple values for one field:
            if type(storage[field]) == type([]):
                form[field] = ()
                for item in storage[field]:
                    if item.filename:
                        form[field]=\
                            _tupleMerge(form[field], item)
                    else:
                        form[field]=\
                            _tupleMerge(form[field], item.value)
            ## or a single value for the field:
            elif storage[field].filename:
                form[field]=storage[field]
            else:
                form[field]=storage[field].value
        self.form = form

