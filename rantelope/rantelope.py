#!/usr/bin/python2.4
"""
Rantelope!
(c)2002-2006 Sabren Enterprises, Inc.
This program is free software,
licensed under the GNU GPL.
"""

from clerks import Schema, MockClerk
from optparse import OptionParser
from pytypes import DateTime
from sixthday import Auth
from strongbox import *
import clerks as arlo
import crypt
import ransacker
import sixthday
import os
import sys
import unittest
import zebra
import storage
import sqlGuru
from weblib import RequestBuilder, Response
from sesspool import Sess, InMemorySessPool


ROOT = "/home/sabren/web/withoutane.com/"

# NOTE: all ID attributes must default
# to "None" for SQLite's autonumbering
# this doesn't effect MySQL's auto_increment 
auto = None

# * parse rant files
class RantParser(object):
    def __init__(self, path):
        self.url = path
        self._parse(open(path).read())

    def _parse(self, data):
        self.data = []
        lines = data.split("\n")
        topline = lines[0]
        if topline.startswith("["):
            # new style dates
            self.date, self.title = topline.split("]",1)
            self.date = self.date + "]"
        else:
            self.date, self.title = topline.split(" ",1)
        para = []
        for line in lines[1:]:
            if line.strip()=="":
                if para:
                    self.data.append(" ".join(para))
                para = []
            else:
                para.append(line + "\n")
        if para:
            self.data.append(" ".join(para))



def toHTML(rant, comments):
    res = []
    for chunk in rant.data:
        if not chunk.strip(): continue
        if chunk.strip().startswith("<"):
            res.append(chunk)
        else:
            res.append("<p>%s</p>" % chunk)
    return "".join(res)


# * Author
class Author(Strongbox):
    ID = attr(long, default=auto)
    fname = attr(str)
    lname = attr(str)
    email = attr(str)
    homepage = attr(str)
    username = attr(str)
    cryptpwd = attr(str)
    
    def set_password(self, value):
        #@TODO: randomize the crypt salt
        self.cryptpwd = crypt.crypt(value, "xx")
    def get_password(self, value):
        raise ValueError, "passwords are encrypted"
    def isPassword(self, value):
        return self.cryptpwd == crypt.crypt(value, self.cryptpwd[:2])
    
    
# * Story

class TagTest(unittest.TestCase):
    def test(self):
        s = Story(csvtags=" apples, banANA CREME pie, etc." )
        assert s.tags == ["apples", "banana creme pie", "etc."]
        s = Story()
        assert s.tags == []


class Story(Strongbox):
    """
    A document, blog entry, or other text.
    """
    ID = attr(long, default=auto)    
    channel = link(forward)
    category = link(forward)
    posted = attr(DateTime, default="now")
    title = attr(str)
    url = attr(str)
    description = attr(str)
    author = link(Author)
    csvtags = attr(str)
    location = attr(str, default="internal", okay=["internal","external"])

    def get_tags(self):
        if self.csvtags:
            return [t.strip().lower() for t in self.csvtags.split(",")]
        return []

    def get_content(self):
        if self.location =="internal":
            return self.description
        else:
            return toHTML(RantParser(ROOT + self.url), [])

    def get_updated(self):
        #@TODO: capture timezone from config?
        return self.posted.to_datetime().isoformat()+"-05:00"
    
# * Category
class Category(Strongbox):
    """
    A category of story.
    """
    ID = attr(long, default=auto)
    channel = link(forward)
    name = attr(str)
    

# * xml stuff for Channel.
## @TODO: xml/xslt stuff should get its own file (??)
## try:
##     plainXSLT = open("plain.xsl").read()
## except:
##     raise Warning, "what happened to plain.xsl?!?!?!"

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
  

# * Channel
class Channel(Strongbox):
    """
    A collection of Stories. (A blog, for example)
    """
    ID = attr(long, default=auto)
    title = attr(str)
    url = attr(str)
    description = attr(str)
    rssfile = attr(str, okay="([^/]+.rss|^$)" )
    htmlfile = attr(str, okay="([^/]+|^$)" )
    template = attr(str, default="withoutane.zb") #default=plainXSLT)
    stories = linkset(Story, "channel")
    categories = linkset(Category, "channel")
    path = attr(str, default="./out/")

    def sort(self):
        self.stories.sort(lambda a,b: -cmp(a.posted,b.posted))

    def toRSS(self):
        self.sort()
        return zebra.fetch("rss", BoxView(self))

    def toAtom(self):
        self.sort()
        return zebra.fetch("atom.zb", BoxView(self))

    def OLD_toHTML(self, input=None):  #@TODO: get rid of this?
        RSS = input or self.toRSS()
        res = transform(RSS, self.template)
        res = "\n".join(res.split("\n")[1:])
        return res

    def toHTML(self, input=None):
        self.sort()
        model = {}
        bv = BoxView(self)
        for k in bv.keys():
            model[k] = bv[k]
        model["stories"] = [BoxView(s) for s in self.stories[:5]]
        return zebra.fetch(self.template, model)
        

    def archiveList(self):
        res = []
        self.sort()
        for s in self.stories[10:]:
            url = s.url
            if not url.startswith("rants"):
                url = "rants/" + url
            res.append('<p class="archive"><a href="/' + url + '">'
                         + s.title + "</a></p>")
        return "\n".join(res)


    def get_updated(self):
        self.sort()
        if self.stories:
            return self.stories[0].updated
        else:
            return None

    def writeFiles(self):
        """
        """
        rss = self.toRSS()
        if self.rssfile:
            print >> open(self.path + self.rssfile, "w"), rss            
        if self.htmlfile and self.template:
            print >> open(self.path + self.htmlfile, "w"), self.toHTML()
        #@TODO: clean this up!!
        print >> open(self.path + "archive.inc.php", "w"), self.archiveList()
        print >> open(self.path + "feed.atom", "w"), self.toAtom()
        
        

        
# * db mapping
Story.channel.type = Channel
Story.category.type = Category
Category.channel.type = Channel

SCHEMA = Schema({
    Channel: "rnt_channel",
    Channel.stories: "channelID",
    Channel.categories: "channelID",
    Category: "rnt_category",
    Category.channel: "channelID",
    Story: "rnt_story",
    Story.author: "authorID",
    Story.channel: "channelID",
    Story.category: "categoryID",
    Author: "rnt_author",
})



# * AuthorAuth
"""
Authentication based on rantelope Author class
"""

class AuthorAuthTest(unittest.TestCase):
    
    def test_login(self):

        clerk = MockClerk(SCHEMA)
        clerk.store(Author(username='fred', password='wanda'))
        sess = Sess(InMemorySessPool(),RequestBuilder().build(),Response())
        aa = AuthorAuth(sess, clerk)
        
        assert aa.fetch(1).username == 'fred'
        aa.login(1)
        assert aa.user.username == 'fred'

        assert aa.validate({"username":"fred", "password":"wanda"})
        assert not aa.validate({"username":"fake", "password":"spam"})
        


class AuthorAuth(Auth):

    def __init__(self, sess, clerk):
        self.clerk = clerk
        Auth.__init__(self, sess, {})

    def prompt(self, message, action, hidden):
        model = {"message": message,
                 "action": action,
                 "hidden": hidden, }
        #@TODO: make this return a string
        self._sess._response.write(zebra.fetch("login", model))
        

    def fetch(self, key):
        #@TODO: need to define strict semantics for *Auth.fetch()
        self.user = self.clerk.fetch(Author, key)
        return self.user

    def validate(self, dict):
        res = None
        match = self.clerk.match(Author, username=dict.get("username"))
        assert len(match) < 2, "wtf? multiple Authors with this username!"
        if match and match[0].isPassword(dict.get("password")):
            res = match[0].ID
        return res
    
# * StoryIndex
class StoryIndexTest(unittest.TestCase):
    
    def test_basics(self):
        c = MockClerk(SCHEMA)
        idx = StoryIndex(c, ":memory:")

        s1 = c.store(Story(title="onedog", description="a big dog"))
        s2 = c.store(Story(title="twodog", description="dog eat dog"))
        s3 = c.store(Story(title="onecat", description="a fat cat"))

        idx.addStory(s1)
        idx.addStory(s2)
        idx.addStory(s3)

        dogs = idx.match("dog")
        cats = idx.match("cat")
        assert len(dogs)==2, dogs        
        assert len(cats)==1, cats
        
        # and check scoring:
        assert dogs[0].title=="twodog"
        assert dogs[1].title=="onedog"

        blank = c.store(Story(title="", description=""))
        idx.addStory(blank)


class StoryIndex(ransacker.SQLiteIndex):

    def __init__(self, clerk, filename):
        self.clerk = clerk
        super(StoryIndex, self).__init__(filename)

    def addStory(self, story):
        if story.title or story.description:
            self.addDocument(story, story.title + " " + story.description)
        else:
            # @TODO: this store a blank code is a kludge
            # I'm doing it because by removing the REPLACE INTO
            # for registerPage, _doIndexing  calls commit()
            # even though nothing has been done yet, which
            # causes a crash.
            self.addDocument(story, "_")

    def _registerPage(self, story):
        assert story.ID, "must have an ID"                
        
    def _getPageID(self, story):
        return story.ID
    
    def score(self, word):
        sql =(
            """
            SELECT pageID, count
            FROM idx_freq f, idx_word w
            WHERE f.wordID=w.ID and w.word='%s'
            ORDER BY count DESC
            """ % self._esc(word))
        self.cur.execute(sql)
        return tuple([ (self.clerk.fetch(Story, ID) ,count)
                       for ID, count in self.cur.fetchall()])

    def search(self, query):
        #@TODO: strongboxen need to be hashable!
        matchIDs = {}
        for term in query.split():
            if not term.strip(): continue
            for story,score in self.score(term):
                matchIDs.setdefault(story.ID, 0)
                matchIDs[story.ID] += score

        matchIDs = matchIDs.items()
        matchIDs.sort(lambda a,b: cmp(a[1],b[1]))
        return [self.clerk.fetch(Story, ID) for ID,score in matchIDs]
    


        
# * RantelopeApp

class RantelopeApp(sixthday.AdminApp):

    def __init__(self, clerk, input, user):
        super(RantelopeApp, self).__init__(clerk, input)
        self.user = user

        
    def act_(self):
        self.list_channel()

    ## authors #########################

    def list_author(self):
        authors = [BoxView(a) for a in self.clerk.match(Author)]
        self.generic_list(authors, "lst_author")

    def create_author(self):
        self.generic_create(Author, "frm_author")

    def edit_author(self):
        self.generic_show(Author, "frm_author")

    def save_author(self):
        a = self._getInstance(Author)
        if self.input.get("password"):
            a.password = self.input["password"]
        self.clerk.store(a)
        self.redirect(action="list&what=author")


    ## channels ########################

    def list_channel(self):
        channels = [BoxView(c) for c in self.clerk.match(Channel)]
        self.generic_list(channels, "lst_channel")

    def create_channel(self):
        self.generic_create(Channel, "frm_channel")
        
    def edit_channel(self):
        self.generic_show(Channel, "frm_channel")

    def show_channel(self):
        chan = self.clerk.fetch(Channel, long(self.input["ID"]))
        model = {"errors":[]}
        model.update(BoxView(chan))

        print >> self, zebra.fetch("sho_channel", model)

    def save_channel(self):
        chan = self.generic_save(Channel)
        if chan.stories:
            chan.writeFiles()
        self.redirect(action='show&what=channel&ID=%s' % chan.ID)

    ## categories ######################

    def save_category(self):
        cat = self.generic_save(Category)
        self.redirect(action='show&what=channel&ID=%s' % cat.channel.ID)

    def edit_category(self):
        self.generic_show(Category, "frm_category")  

    ## stories #########################

    def studyChannel(self, channelID):
        assert channelID, "must supply valid channelID"
        chan = self.clerk.fetch(Channel, channelID)
        self.model["categories"] = [(c.ID, c.name) for c in chan.categories]
        # @TODO: will need to limit number of past stories soon.
        self.model["stories"] = [BoxView(s) for s in chan.stories]
	self.model["stories"].sort(lambda a,b: -cmp(a["posted"], b["posted"]))
        return chan

    def create_story(self):
        c = self.studyChannel(self.input.get("channelID"))
        self.model["siteurl"] = c.url
        self.generic_create(Story, "frm_story")
        
    def edit_story(self):
        s = self.clerk.fetch(Story, self.input["ID"])
        c = self.studyChannel(s.channel.ID)
        self.model["siteurl"] = c.url
        self.model["stories"] = []
        self.model["channelID"] = c.ID
        self.generic_show(Story, "frm_story")

    def save_story(self):
        ## first save to database:
        
        c = self.studyChannel(self.input.get("channelID"))
        """
        ugh. this next part has to come after the studyChannel call
        or you can't update. that's messed up. I think it's
        because getInstance doesn't deal with the arlo caching
        correctly or something. But it really doesn't matter
        since this whole _getInstance thing needs to go away
        completely anyway.
        """
        story = self._getInstance(Story)
        c.stories << story
        if not story.author:
            story.author = self.user
        self.clerk.store(story)

        ## go back to the channel:
        self.redirect(action='create&what=story&channelID='
                            + str(story.channel.ID))        
        
    def delete_story(self):
        ## first save to database:
        story = self._getInstance(Story)
        #@TODO: why is story.author != self.user!? they should be identical!
        if story.author.username == self.user.username:
            self.clerk.delete(Story, story.ID)
        else:
            assert 0, "this story belongs to " + story.author.username

        ## go back to the channel:
        self.redirect(action='create&what=story&channelID='
                            + str(story.channel.ID))        
        
    def show_story(self):
        self.generic_show(Story, "sho_story")

    ## publishing ######################
        
    def act_publish(self):
        ## now write the XML file:
        publish(self.clerk, self.input["channelID"])
        self.redirect(action="create&what=story&status=published&channelID="
                      + self.input["channelID"])


# * runTests
def runTests(*x):
    sys.argv.remove("--test")
    unittest.main()


# * addFile
def sqlDate(rantDate):
    if rantDate.startswith("["):
        # new style: [2006.0210 20:17]
        return "%s-%s-%s %s" % (rantDate[1:5], rantDate[6:8],
                                rantDate[8:10], rantDate[11:-1])
    else:
        # old style: 0210.2006
        return "%s-%s-%s" % (rantDate[5:], rantDate[:2], rantDate[2:4])

assert sqlDate("0210.2006") == "2006-02-10"
assert sqlDate("[2006.0210 20:16:23]") == "2006-02-10 20:16:23", \
       sqlDate("[2006.0210 20:16:23]")

def addFile(filename):
    """
    add a new file to the system
    """
    if os.path.exists(".rantelope"):
        path = open(".rantelope").read().strip()
        x =os.path.join(path, filename)
        while x.startswith("/"): x=x[1:]
        print x
        sto = storage.MySQLStorage(sqlGuru.dbc)
        rant = RantParser(ROOT + x)
        row = {
            "channelID": 1,
            "categoryID":3,
            "posted": sqlDate(rant.date),
            "title": rant.title,
            "url": x,
            "authorID": 2,
            "location": "external",
            }
        sto.store("rnt_story", **row)
    else:
        print ".rantelope file not found: can't determine relative path"

# * publish
def publish(CLERK, channelID):
    chan=CLERK.fetch(Channel, channelID)
    chan.writeFiles()
    

# * parseCommandLine

def parseCommandLine():
    parser = OptionParser()
    parser.add_option("--test", action="callback", callback=runTests)
    parser.add_option("-p", "--publish", action="store_true", dest="publish", default=False)
    parser.add_option("--add", action="store", dest="addFile", default=None)
    (options, args) = parser.parse_args()
    
    return options, args

# * --
if __name__=="__main__":
    options, args = parseCommandLine()
    if options.addFile:
        addFile(options.addFile)
    if options.publish:
        #@TODO: fix path kludge
        os.chdir("/home/sabren/web/withoutane.com/rantelope")
        from sqlRantelope import clerk
        clerk.schema = SCHEMA
        #import pdb; pdb.set_trace()
        publish(clerk, 1)
