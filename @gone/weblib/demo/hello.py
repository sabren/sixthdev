

if REQ.get("name"):
    if REQ["name"]=="jump":
        RES.redirect("http://www.twistedmatrix.com/")
    else:
        print >> RES, "<h2>hello, %s!</h2>" % REQ["name"]

else:
    print >> RES, '<h2>what is your name?</h2>'
    print >> RES, '<form method="post">'
    print >> RES, '<input type="text" name="name">'
    print >> RES, '<input type="submit" value="submit">'
    print >> RES, '</form>'
