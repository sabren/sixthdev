# experimental webli driver for mod_python

from mod_python import apache
import sys
import os.path
sys.path = [".", '/home/sabren/web/blogdrive.com/lib'] + sys.path
import weblib

class ModPythonEngine(weblib.Engine):
    def setPathInfo(self):
        if not self.request.environ.get("SCRIPT_NAME"):        
            if (type(self.script) == type("")):
                self.request.environ["PATH_INFO"] = "UNKNOWN_SCRIPT.py"
            else:
                self.request.environ["PATH_INFO"] = self.script.name
        


def handler(req):

    e=apache.build_cgi_env(req)
    #req.send_http_header()
    env = {}
    for bleh in e.keys():
        env[bleh]=e[bleh]
        #print >> req, bleh, ":", e[bleh], "<br>"
    #return apache.OK


    wreq=weblib.Request(content=req.read(),
                        environ=env)

    eng = ModPythonEngine(request=wreq,script="")
    eng.start()
    dir = os.sep.join(req.filename.split(os.sep)[:-1]) + os.sep
    os.chdir(dir)
    if os.path.exists(dir + ".weblib.py"):
        whichfile= dir + ".weblib.py"
        eng.execute(open(whichfile))
    if (eng.result ==eng.SUCCESS) or (eng.result is None):
        whichfile=req.filename
        eng.execute(open(whichfile))
    eng.stop()


    if eng.result in (eng.SUCCESS, eng.EXIT):
        import string
        headers = eng.response.getHeaders()
        for i in string.split(headers, "\n"):
            if i != "":
                header = string.split(i, ":")
                req.headers_out[header[0]] = header[1]
                if string.lower(header[0]) == 'content-type':
                    req.content_type = header[1]
                if string.lower(header[0]) == 'status':
                    req.status = int(header[1])
     
        req.send_http_header()
        req.write(eng.response.buffer)
        return apache.OK

    else:
        ## print debug output
        print >> req, weblib.trim("""
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
          """)

        if eng.result == eng.FAILURE:
            print >> req, "<b>assertion failure:</b>", eng.error
            print >> req, "</body>\n</html>"

        elif eng.result == eng.EXCEPTION:

            ## html error message #################################

            print >> req, "<b>uncaught exception while running %s</b><br>" \
                  % whichfile
            print >> req, '<pre class="traceback">' \
                  + weblib.htmlEncode(eng.error) + "</pre>"

            print >> req, "<b>script input:</b>"

            print >> req, '<ul>'
            print >> req, '<li>form: %s</li>' % eng.request.form
            print >> req, '<li>querystring: %s</li>' % eng.request.querystring
            print >> req, '<li>cookie: %s</li>' % eng.request.cookie
            print >> req, '</ul>'

            print >> req, '<b>session data:</b><br>'
            print >> req, '<ul>'

            for item in eng.sess.keys():
                print >> req, '<li>', item, ': '
                try:
                    print >> req, eng.sess[item]
                except:
                    print >> req, '(can\'t unpickle)'
                print >> req, '</li>'
            print >> req, '</ul>'
	
            print >> req, "<b>script output:</b>"
            print >> req, '<pre class="output">' + \
              weblib.htmlEncode(eng.response.getHeaders()) + \
              weblib.htmlEncode(eng.response.buffer) + \
              "</pre>"

        print >> req, "<hr>"
        print >> req, '<a href="http://weblib.sourceforge.net/">weblib</a> ' + \
          '(c) copyright 2000-2001 ' + \
          '<a href="http://www.zike.net/">Zike Interactive</a>. ' + \
          'All rights reserved.'
        print >> req, "</body>"
        print >> req, "</html>"
        return apache.OK
