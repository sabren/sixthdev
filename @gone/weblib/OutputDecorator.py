"""
formats Engine output (mostly for error-trapping)
"""
from handy import trim
from weblib import Engine
from weblib import htmlEncode

class OutputDecorator(object):

    def __init__(self, eng):
        self.eng = eng
        
    def getHeaders(self):
        return self.eng.response.getHeaders()

    def getBody(self):
        if self.eng.hadProblem():
            res = self.errHeader()
            if self.eng.result == Engine.FAILURE:
                res += "<b>assertion failure:</b> %s" % self.eng.error
            elif self.eng.result == Engine.EXCEPTION:
                res +=  self.errTraceback()
            res += self.errFooter()
            return res
        else:
            return self.eng.response.buffer

    #@TODO: consolidate html and plain text error reports?
    def sendError(self):
        SITE_MAIL = self.eng.globals["SITE_MAIL"]
        SITE_NAME = self.eng.globals["SITE_NAME"]
        assert SITE_MAIL is not None, "must define SITE_MAIL first!"
        hr = "-" * 50 + "\n"
        msg = trim(
            """
            To: %s
            From: cgi <%s>
            Subject: uncaught exception in %s

            """ % (SITE_MAIL, SITE_MAIL, SITE_NAME))
        msg += "uncaught exception in %s\n\n" % self.eng.request.pathInfo
        msg += hr
        msg += self.eng.error
        msg += hr
        msg += "FORM: %s\n"  % self.eng.request.form
        msg += "QUERYSTRING: %s\n" % self.eng.request.query.string
        msg += "COOKIE: %s\n" % self.eng.request.cookie

        if hasattr(self, "sess"):
            msg = msg + "SESSION DATA:\n"
            for item in self.eng.sess.keys():
                msg += item + ': '
                try:
                    msg += self.eng.sess[item] + "\n"
                except:
                    msg += "(can't unpickle)\n"
        else:
            msg += "NO SESSION DATA\n"
        msg += hr
        msg += "OUTPUT:\n\n"
        msg += self.eng.response.getHeaders() + "\n"
        msg += self.eng.response.buffer + "\n"
        msg += hr

        handy.sendmail(msg)

    def errTraceback(self):
        res = '<b>uncaught exception while running %s</b><br>\n'\
              % self.eng.request.pathInfo
        res+= '<pre class="traceback">\n' \
              + htmlEncode(self.eng.error) + "</pre>\n"
        res+= "<b>script input:</b>\n"
        res+= '<ul>\n'
        res+= '<li>form: %s</li>\n' % self.eng.request.form
        res+= '<li>querystring: %s</li>\n' % self.eng.request.query.string
        res+= '<li>cookie: %s</li>\n' % self.eng.request.cookie
        res+= '</ul>\n'
        if self.eng.globals.has_key("SESS"):
            res+= '<b>session data:</b><br>\n'
            res+= '<ul>\n'
            for item in self.eng.globals["SESS"].keys():
                res+= '<li>', item, ': '
                try:
                   res+= self.eng.globals["SESS"][item]
                except:
                   res+= '(can\'t unpickle)'
                res+= '</li>\n'
            res+= '</ul>\n'
        res+= "<b>script output:</b>\n"
        res+= '<pre class="output">\n' + \
              htmlEncode(self.eng.response.getHeaders()) + \
              htmlEncode(self.eng.response.buffer) + \
              "</pre>\n"
        return res

    def errHeader(self):
        return trim(
            '''
            <html>
            <head>
            <title>weblib.cgi exception</title>
            <style type="text/css">
                body, p {
                   background: #cccccc;
                   font-family: verdana, arial;
                   font-size: 75%;
                }
                pre { font-size: 120%; }
                pre.traceback { color: red; }
                pre.output{ color : green }
            </style>
            </head>
            <body>
            ''')

    def errFooter(self):
        return trim(
            '''
            <hr>
            <a href="http://www.tangentcode.com/">weblib</a>
            (c) copyright 2000-2003 
            <a href="http://www.sabren.com/">Sabren Enterprises, Inc</a>. 
            All rights reserved.
            </body>
            </html>
            ''')
