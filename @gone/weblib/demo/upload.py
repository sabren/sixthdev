import sys, weblib

def showForm():
    print weblib.trim(
        """
        This page is a complete waste of bandwidth. You upload
        a file, and it sends it back to you.
        
        <form method="POST" enctype="multipart/form-data"
              action="upload.py?upload=1">
           <input type="file" name="upfile" size="50">
           <input name="action" type="submit" value="upload">
        </form>
        """)

if weblib.request.get("upload"):
    weblib.response.contentType=weblib.request["upfile"].type
    weblib.response.write(weblib.request["upfile"].file.read())
else:
    showForm()

