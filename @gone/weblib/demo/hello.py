
if REQ.get("name"):
    print >> RES, "<h2>hello, %s!</h2>" % REQ["name"]
else:
    print >> RES, '<h2>what is your name?</h2>'
    print >> RES, '<form method="post">'
    print >> RES, '<input type="text" name="name">'
    print >> RES, '<input type="submit" value="submit">'
    print >> RES, '</form>'
