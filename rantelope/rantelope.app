"""
Rantelope!
(c)2002 Sabren Enterprises, Inc.
This program is free software,
licensed under the GNU GPL.
"""
__ver__="$Id$"

from Node import Node
from strongbox import *
import sixthday
import zebra


### default template ################################

plainXSLT =\
'''\
<xsl:stylesheet version="1.0"
   xmlns:rss="http://backend.userland.com/rss2"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   
   <xsl:template match="rss:channel">
     <html>
       <head>
         <title><xsl:value-of select="rss:title"/></title>
         <style type="text/css">
         body {
            font-family: arial, helvetica;
            font-size: 10pt;
            background: white;
         }
         h1 {
            color: red;
         }
         h2 {
            background: black;
            color: white;
            font-size: 12pt;
         }
         div.post {
            border-bottom: solid gray 1px;
            margin-bottom: 10px;
            width: 500px;
         }
         </style>
       </head>
       <body>
         <h1><xsl:value-of select="rss:title"/></h1>
         <p><i><xsl:value-of select="rss:description"/></i></p>

         <xsl:for-each select="rss:item">
            <div class="post">
              <h2><xsl:value-of select="rss:title"/></h2>
              <xsl:value-of select="rss:description"/>
            </div>
         </xsl:for-each>
       </body>
     </html>
   </xsl:template>
   
</xsl:stylesheet>
'''

def transform(xml, xsl):
    """
    A simple wrapper for 4XSLT.
    """
    from Ft.Xml.Xslt.Processor import Processor
    from Ft.Xml.InputSource import DefaultFactory
    proc = Processor()
    xslObj = DefaultFactory.fromString(xsl, "http://rantelope.com/")
    proc.appendStylesheet(xslObj)
    xmlObj = DefaultFactory.fromString(xml)
    return proc.run(xmlObj)


### object model ####################################


class Comment(Strongbox):
    ID = attr(long)
    storyID = attr(long)
    name = attr(str)
    mail = attr(str)
    link = attr(str)
    note = attr(str)   

class Story(Strongbox):
    ID = attr(long)
    channelID = attr(long)
    title = attr(str)
    link = attr(str)
    description = attr(str)
    comments = linkset(Comment)
    
class Channel(Node):
    ID = attr(long)
    parentID = attr(long, default=0)
    title = attr(str)
    link = attr(str)
    description = attr(str)
    rssfile = attr(str, okay="([^/]+.rss|^$)" )
    htmlfile = attr(str, okay="([^/]+.html|^$)" )
    template = attr(str, default=plainXSLT)
    stories = linkset(Story)
    path = attr(str, default="./out/") # hard-coded for now.    

    def toRSS(self):
        return zebra.fetch("rss", BoxView(self))

    def toHTML(self, input=None):
        rss = input or self.toRSS()
        return transform(rss, self.template)

    def writeFiles(self):
        rss = self.toRSS()
        if self.rssfile:
            print >> open(self.path + self.rssfile, "w"), rss
        if self.htmlfile and self.template:
            print >> open(self.path + self.htmlfile, "w"), self.toHTML(rss)
                

### interface #######################################

class RantelApp(sixthday.AdminApp):

    def act_(self):
        self.list_channel()

    ## channels ########################

    def list_channel(self):
        channels = [BoxView(c) for c in self.clerk.match(Channel, parentID=0)]
        self.generic_list(channels, "lst_channel")

    def create_channel(self):
        self.generic_create(Channel, "frm_channel")
        
    def edit_channel(self):
        self.generic_show(Channel, "frm_channel")

    def show_channel(self):
        chan = self.clerk.fetch(Channel, long(self.input["ID"]))
        chan.clerk = self.clerk
        model = {"errors":[]}
        model.update(BoxView(chan))
        model["kids"]= [BoxView(k) for k in chan.kids]
        model["crumbs"]= [BoxView(k) for k in chan.crumbs]
        print >> self, zebra.fetch("sho_channel", model)


    def save_channel(self):
        chan = self.generic_save(Channel)
        chan.writeFiles()
        self.redirect(action='show&what=channel&ID=%s' % chan.ID)

    ## stories #########################

    def create_story(self):
        assert self.input["channelID"], "must supply channelID"
        self.generic_create(Story, "frm_story")
        
    def edit_story(self):
        self.generic_show(Story, "frm_story")

    def save_story(self):
        ## first save to database:
        story = self.generic_save(Story)

        ## now write the XML file:
        chan=self.clerk.fetch(Channel, self.input["channelID"])
        chan.writeFiles()

        ## go back to the channel:
        self.redirect(action='show&what=channel&ID='
                            + str(story.channelID))
        
    def show_story(self):
        self.generic_show(Story, "sho_story")

    ## comments ########################
        
    def save_comment(self):
        cmt = self.generic_save(Comment)
        self.redirect(action='show&what=story&ID='
                            + str(cmt.storyID))


### main code #######################################

if __name__=="__main__":

    import arlo, storage, sqlRantelope
    dbmap = {Channel: "rnt_channel",
             Channel.__attrs__["stories"]: (Story, "channelID"),
             Story: "rnt_story",
             Story.__attrs__["comments"]: (Comment, "storyID"),
             Comment: "rnt_comment"}
    CLERK = arlo.Clerk(storage.MySQLStorage(sqlRantelope.dbc), dbmap)
    
    ## now just run the app!
    print >> RES, RantelApp(CLERK, REQ).act()

