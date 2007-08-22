
"""
Tinderblaze - read a trailblazer narrative data from a tinderbox outline

Tinderbox files (*.tbx) are xml, but since they seem to have one
tag per line, I didn't bother with an xml parser.

"""

import sys
import os
from PlainTextBlazeHound import parseBlaze, loadTBFile
from Solution import Solution
from handy import xmlEncode
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.lexers import JavascriptLexer
from pygments.formatters import HtmlFormatter
import cStringIO


#@TODO: unhardcode input filename

inputStream = (open(sys.argv[1]) if len(sys.argv) > 1
               else open('p:/keep/projects/brickslayer.tbx'))

HTMLformat = HtmlFormatter(cssclass="source")
# print HTMLformat.get_style_defs() # dump css rules


trail = Solution()

loadBlaze = "@="
showBlaze = "@+"
hideBlaze = "@-"
snapBlaze = "@!"


def wipeout(dir):
    os.system("rm -rf %s" % dir)
    os.mkdir(dir)


mainDir = "/Users/michal/sites/javascriptgamer.com/brickslayer"
codeDir = mainDir + "/code"

# careful! the snapdir gets wiped out!
snapDir = mainDir + "/snap"
wipeout(snapDir)

# same with the traildir
trailDir = mainDir + "/trail"
wipeout(trailDir)


os.chdir(codeDir)

textMode = False
textBuff = [] # cstringio?


prompt = '<span class="gp">&gt;&gt;&gt; </span>'


def htmlDecode(s):
    return s.replace("&apos;","'").replace("&quot;",'"').replace("&lt;","<").replace("&gt;",">")


class Lesson(object):
    def __init__(self, snapName, title):
        self.title = title
        self.content = cStringIO.StringIO()
        self.summary = ''
        self.snapName = snapName
        
    def showText(self, depth, text):
        if depth == 1:
            self.summary = htmlDecode(text)
            return ''
        else:
            return '<div class="detail">%s</div>' % htmlDecode(text)

    def write(self, text):
        self.content.write(text)



trash = Lesson('trash','trash')
lessons = []
contents = []
out = trash
static = {} # static files
lastSnap = None
prev, next = {}, {}
title = None
trigger = {} # depth trigger


depth = 0
for line in inputStream:

    if textMode:
        
        if line.count("</text>"):
            textMode = False
            textBuff.append(line[:line.find("</text>")])
            print >> out, out.showText(depth, "".join(textBuff))
        else:
            textBuff.append(line)

    elif line.startswith("<text >"):
        if line.count("</text>"):
            print >> out, out.showText(depth, line[7:line.find("</text>")])
        else:
            textBuff = [line[7:]]
            textMode = True
        


    # handle nesting
    elif line.startswith("<item"):
        depth += 1
    elif line.startswith("</item"):
        depth -= 1
        if trigger.get(depth):
            trigger[depth]()
            trigger[depth] = None


    # deal with headline(name) for each note
    elif line.startswith('<attribute name="Name"'):
        name = line.split(">")[1].split("<")[0]

        if name.startswith("#"):
            out = trash

        elif name.startswith(";"):
            # this is so we can add paragraphs without headlines
            print >> out, "<p>%s</p>" % name[2:]

        elif name.upper().startswith("@TODO"):
            print >> out, '<h1 style="background:#FF0;color:black;font-size:12pt">%s</h1>' % name

        # new lesson marker
        elif name.startswith('% '):
            oldTitle = title
            snapName, title = [s.strip() for s in name.split("%") if s]
            out = Lesson(snapName, title)
            if lastSnap:
                prev[snapName] = (lastSnap, oldTitle)
                next[lastSnap] = (snapName, title)
            else:
                prev[snapName] = None # handle first one
            next[snapName] = None # handle last one
            lastSnap = snapName
            lessons.append(out)
            depth = 1

        # blazes
        elif name.startswith(loadBlaze):
            root, filename = name[2:].strip().split(" ",1)
            # handle tb files
            if os.path.exists(filename + ".tb"):
                tree = trail.addChild(root, loadTBFile(filename+'.tb'))
                tree.outFile = filename
                tree.hideAll()
            # handle static files
            elif os.path.exists(filename):
                static[filename] = open(filename).read()
            else:
                raise Exception("not found: %s" % filename)

        elif name.startswith(showBlaze):
            path = parseBlaze(name, showBlaze)
            try:
                trail[path].show()
            except KeyError:
                raise KeyError( path)

            code = trail[path].snapShot()


            # add a fake <? php so the syntax highlight works
            snip = False
            if path.startswith("php") and not (code.startswith("<?php")):
                code = "<?php\n"+code
                snip = True

            
            html = highlight(code,
                             get_lexer_for_filename(trail[path.split(".")[0]].outFile),
                             HTMLformat)

            # remove the fake <? php
            if snip:
                match = '<span class="cp">&lt;?php</span>'
                point = html.find(match)
                html = html[:point] + html[point+len(match):]
            print >> out, html
            

        elif name.startswith(hideBlaze):
            path = parseBlaze(name, hideBlaze)
            print >> out, '<pre class="hide">%s</pre>' % xmlEncode(trail[path].snapShot())
            trail[path].hide()

        elif name.startswith("&gt; "):
            html = highlight(htmlDecode(name[5:]), JavascriptLexer(), HTMLformat)
            cutPoint = html.find("<span")
            print >> out, html[:cutPoint] + prompt + html[cutPoint:]

        elif name.startswith(snapBlaze):
            # make snapshots in directory snap/snapName
            snapName = parseBlaze(name, snapBlaze)
            snapPath = os.path.join(snapDir, snapName)
            os.mkdir(snapPath)
            for item in trail.blazes.values():
                if item.visible:
                    fileName = item.fileName
                    f = open(os.path.join(snapPath, item.outFile), "w")
                    f.write(item.snapShot())
                    f.close()
            
            for k,v in static.items():
                f = open(os.path.join(snapPath, k), 'wb')
                f.write(v)
                f.close()

            os.chdir(snapDir)
            os.system("tar -czf %s.tgz %s" % (snapName, snapName))
            os.system("mv %s.tgz %s" % (snapName, trailDir))
            os.chdir(codeDir)

            out.minigame = trail['html.console'].snapShot() + trail['html.onload'].snapShot()

        elif name.lower().startswith("firebug"):
            print >> out, '<div class="firebug">'
            print >> out, "<h%s>%s</h%s>" % (depth, name, depth)
            trigger[depth-1] = lambda : out.write('</div>')
        
        else:
            print >> out, "<h%s>%s</h%s>" % (depth, name, depth)
            



implan = cStringIO.StringIO()
print >> implan, "<h2>Development Trail</h2>"


template = open(os.path.join(mainDir,'template.html')).read()

for num, each in enumerate(lessons):
    trailFileName = "%02i-%s.html" % (num, each.snapName)
    trailFile = open(os.path.join(trailDir, trailFileName), 'w')

    navBar = ['<div style="background: #CCCCCC; height: 25px;">']
    if prev[each.snapName]:
        navBar.append('<span style="float:left">previous: <a href="%02i-%s.html">%s</a></span>'
                      % (num-1, prev[each.snapName][0], prev[each.snapName][1]))
    if next[each.snapName]:
        navBar.append('<span style="float:right">next: <a href="%02i-%s.html">%s</a></span>'
                      % (num+1, next[each.snapName][0], next[each.snapName][1]))
        
    navBar.append('<br clear="all"/></div>')

    snapName = '%02i-%s' % (num, each.snapName)
    if each.snapName == 'enhancements':
        snapName = 'final'

    print >> trailFile, template % {
        'title' : each.title,
        'htmlTitle' : 'Building Brickslayer - %s' % each.title,
        'summary' : each.summary,
        'content' : each.content.getvalue(),
        'crumbs' : '<a href="./">trail</a> &gt; step %02i' % num,
        'minigame': each.minigame,
        'snapName': snapName, 
        'navBar' : ''.join(navBar),
    }
    
    print >> implan, "<p style='margin:0px; margin-top:5px;font-weight:bold;'>%02i." % num
    print >> implan, '<a href="%s">%s</a></p>' % (trailFileName, each.title)
    if each.summary:
        print >> implan, each.summary
    else:
        print >> implan, "<br/>"




index = open(os.path.join(trailDir, 'index.html'), 'w')
print >> index, template % {
    'title' : "Building Brickslayer",
    'htmlTitle' : 'Building Brickslayer',
    'summary' : "How to make a BreakOut clone in Javascript using Prototype.js",
    'content' : implan.getvalue(),
    'crumbs' : 'trail',
    # each is still the final version...
    'minigame': each.minigame,
    'snapName': 'final',
    'navBar' : '',
}


def listHiddenBlazes(node, path=[]):
    if node.visible:
        for each in node.blazes:
            newpath = path + [each]
            listHiddenBlazes(node[each], newpath)
    else:
        print ".".join(path)

print "hidden nodes:"
print "-------------"
listHiddenBlazes(trail)
