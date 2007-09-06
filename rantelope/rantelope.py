#!/usr/bin/python2.5
"""
Rantelope!
(c)2002-2007 Sabren Enterprises, Inc.
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
#import ransacker
import os
import sys
import unittest
import zebra
import storage
import sqlGuru
from weblib import RequestBuilder, Response
from sesspool import Sess, InMemorySessPool
from strongbox import BoxView
import zebra
import cStringIO
import weblib


ROOT = "/home/sabren/web/withoutane.com/"

# NOTE: all ID attributes must default
# to "None" for SQLite's autonumbering
# this doesn't effect MySQL's auto_increment 
auto = None


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



class Comment(Strongbox):
    ID = attr(long, default=auto)
    topicID = long
    posted = attr(DateTime, default="now")
    name = attr(str)
    mail = attr(str)
    link = attr(str)
    comment = attr(str)
    
    

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
    channel = link(lambda : Channel)
    category = link(lambda : Category)
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
    

class Category(Strongbox):
    """
    A category of story.
    """
    ID = attr(long, default=auto)
    channel = link(lambda : Channel)
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



NUM_ON_FRONTPAGE = 5

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

    def toHTML(self, input=None):
        self.sort()
        model = {}
        bv = BoxView(self)
        for k in bv.keys():
            model[k] = bv[k]
        model["stories"] = [BoxView(s) for s in self.stories[:NUM_ON_FRONTPAGE]]
        return zebra.fetch(self.template, model)
        

    def archiveList(self):
        res = []
        self.sort()
        for s in self.stories[NUM_ON_FRONTPAGE:]:
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
    Comment: "rant_comment",
})




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


class StoryIndex(object): # ransacker.SQLiteIndex):

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
    

def private(f):
    f.private = True
    return f


class RantelopeApp(object):
        
    def __init__(self, clerk, input, user):

        self.input = input
        self.user = user

        # out is just a buffer:
        self.out = cStringIO.StringIO()
        
        self.errors = []
        self.model = {"errors":[]}
        for key in self.input.keys():
            self.model[key] = self.input[key]

        self.clerk = clerk


    ## dispatch methods

    def act(self):
        """
        ex: actor.act();   actor.act('jump')
        returns output buffer built by calls to write()
        """
        action = self.input.get("action", "").replace(" ", "_")              
        assert type(action) == str, "action should be string, but was: %s" % action
        method = getattr(self, "act_" + action, None)
        if not method: method = getattr(self, action, None)
        assert method, "Homie don't know how to %s" % action
        method()
        return self.out.getvalue()

    def act_(self):
        self.list_channel()


    ## create methods 

    def create_author(self):
        self.generic_create(Author, "frm_author")

    def create_channel(self):
        self.generic_create(Channel, "frm_channel")

    def generic_create(self, klass, template):
        self._showObject(klass(), template)

    def create_story(self):
        c = self.studyChannel(self.input.get("channelID"))
        self.model["siteurl"] = c.url
        self.generic_create(Story, "frm_story")

    ## edit/show methods ####################

    def edit_author(self):
        self.generic_show(Author, "frm_author")

    def edit_channel(self):
        self.generic_show(Channel, "frm_channel")

    def edit_category(self):
        self.generic_show(Category, "frm_category")  

    def show_story(self):
        self.generic_show(Story, "sho_story")

    def edit_story(self):
        s = self.clerk.fetch(Story, self.input["ID"])
        c = self.studyChannel(s.channel.ID)
        self.model["siteurl"] = c.url
        self.model["stories"] = []
        self.model["channelID"] = c.ID
        self.generic_show(Story, "frm_story")

    def generic_show(self, klass, template):
        self._showObject(self._getInstance(klass), template)

    def show_channel(self):
        chan = self.clerk.fetch(Channel, long(self.input["ID"]))
        model = {"errors":[]}
        model.update(BoxView(chan))
        self.write(zebra.fetch("sho_channel", model))


    ## list methods #######################

    def list_author(self):
        authors = [BoxView(a) for a in self.clerk.match(Author)]
        self.generic_list(authors, "lst_author")


    def list_comments(self):
        self.generic_list([BoxView(c) for c in self.clerk.match(Comment)][:100], "lst_comment")

    def list_channel(self):
        channels = [BoxView(c) for c in self.clerk.match(Channel)]
        self.generic_list(channels, "lst_channel")

    def generic_list(self, listOfDicts, template):
        self.model["each"] = listOfDicts
        self._runZebra(template)
        

    ## save methods


    def save_author(self):
        a = self._getInstance(Author)
        if self.input.get("password"):
            a.password = self.input["password"]
        self.clerk.store(a)
        self.redirect(action="list_author")

    def save_channel(self):
        chan = self.generic_save(Channel)
        if chan.stories:
            chan.writeFiles()
        self.redirect(action='show_channel&ID=%s' % chan.ID)


    def save_category(self):
        cat = self.generic_save(Category)
        self.redirect(action='show_channel&ID=%s' % cat.channel.ID)

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
        self.redirect(action='create_story&channelID='
                            + str(story.channel.ID))        


    def generic_save(self, klass):
        obj = self._getInstance(klass)
        return self.clerk.store(obj)


    ## delete ###############################

    def delete_story(self):
        ## first save to database:
        story = self._getInstance(Story)
        #@TODO: why is story.author != self.user!? they should be identical!
        if story.author.username == self.user.username:
            self.clerk.delete(Story, story.ID)
        else:
            assert 0, "this story belongs to " + story.author.username

        ## go back to the channel:
        self.redirect(action='create_story&channelID='
                            + str(story.channel.ID))        
        


    ## channels ########################


    def studyChannel(self, channelID):
        assert channelID, "must supply valid channelID"
        chan = self.clerk.fetch(Channel, channelID)
        self.model["categories"] = [(c.ID, c.name) for c in chan.categories]
        # @TODO: will need to limit number of past stories soon.
        self.model["stories"] = [BoxView(s) for s in chan.stories]
	self.model["stories"].sort(lambda a,b: -cmp(a["posted"], b["posted"]))
        return chan


    ## publishing ######################
        
    def act_publish(self):
        ## now write the XML file:
        publish(self.clerk, self.input["channelID"])
        self.redirect(action="create_story&status=published&channelID="
                      + self.input["channelID"])




    ###[ private methods ]###########################################


    def _getInstance(self, klass):
        if self.input.get("ID"):
            obj = self.clerk.fetch(klass, self.input["ID"])
        else:
            obj = klass()
        obj.noisyUpdate(**self.input.form)
        return obj
        

    def _runZebra(self, template):
        try:
            self.write(zebra.fetch(template, self.model))
        except IOError:
            self.complain("unable to load %s.zb" % template)


    def _showObject(self, obj, template):
        self.consult(BoxView(obj))
        self.consult(self.input) # so we can pre-populate via url
        self._runZebra(template)



    ####### This used to be App ######################################
        
    """
    A base class for web pages that act differently based on a parameter.
    """
    
    #@TODO: subclass that uses Signature to pass values to act_XXX?

    """
    App(input) where input=a dict, usually with a key called 'action'.
    
    This class is designed to make it easy to write classes that can
    be called directly through a URL. It's just a base class, and only
    provides enough logic to handle dispatching actions right now.    
    
    The input dict should have a key called "action" that will tell the
    actor what to do. The App subclass must have a method caled act_XXX
    where XXX is whatever "action" mapped to.
    """

    ## public methods ############################################


    def complain(self, problems):
        """
        Generic error handler. Pass it a string or list of strings.
        """
        if type(problems)==type(""):
            probs = [problems]
        else:
            probs = problems
        for prob in probs:
            self.errors.append(prob)
            self.model["errors"].append({"error":prob})

    def consult(self, model):
        """
        updates the App's internal model based on the
        passed in model dictionary.
        """
        for item in model.keys():
            self.model[item] = model[item]


    def redirect(self, url=None, action=None):
        """
        Throws weblib.Redirect
        """
        if not ((url is not None) ^ (action is not None)):
            raise TypeError, "syntax: actor.redirect(url XOR action)"
        if url:
            where=url
            
        else:
            #@TODO: why __weblib_ignore_form__ again?
            where="?action=%s&__weblib_ignore_form__=1" % (action)
            
        raise weblib.Redirect, where


    def write(self, what):
        """
        write something to output..
        """
        self.out.write(what)







############## END OF RantelopeApp #######################################




def runTests(*x):
    sys.argv.remove("--test")
    unittest.main()



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


def publish(CLERK, channelID):
    chan=CLERK.fetch(Channel, channelID)
    chan.writeFiles()
    

def parseCommandLine():
    parser = OptionParser()
    parser.add_option("--test", action="callback", callback=runTests)
    parser.add_option("-p", "--publish", action="store_true", dest="publish", default=False)
    parser.add_option("--add", action="store", dest="addFile", default=None)
    (options, args) = parser.parse_args()
    
    return options, args

def main():
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

if __name__=="__main__":
    main()
