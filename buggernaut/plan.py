"""
plan.py - zikeplan
"""
import sys

# note: for both of the following, get the latest CVS versions,
# NOT the snapshots, because they're too old.

import weblib    # http://sourceforge.net/projects/weblib/
import zdc       # http://sourceforge.net/projects/zdc/
import zikebase  # http://sourceforge.net/projects/zikebase/

## this next line just imports a DB-API compliant database
## connection (actually, it's only been tested with MySQL,
## and currently does rely on MySQL for auto-numbering)
##
## if you're not using MySQL, your best bet is to probably
## override zikebase.ObjectEditor.act_save()
##
import sqlBugs, zdc.drivers.DBAPI2Driver
dbc=zdc.Connection(zdc.drivers.DBAPI2Driver.DBAPI2Driver(sqlBugs.dbc))

class Story(zdc.RecordObject):
    _table = zdc.Table(dbc, "plan_story")
    _defaults = {
        "summary" : '',
        "detail" : '',
        "area" : '',
        "type" : 'story',
        "target" : 'new',
        "status" : 'devel',
        "hrsOrig" : None,
        "hrsCurr" : None,
        "hrsElapsed": None }


def showForm(story):
    if story.ID:
        print "<b>this is 'edit' mode</b>"
    else:
        print "<b>this is 'add' mode</b>"

    print '<form action="plan.py" method="POST">'
    if story.ID:
        print '<input type="hidden" name="ID" value="%s">' % story.ID

    print 'type:'
    cur = dbc.cursor()
    sql = "SELECT type, type, type='%s' from plan_type order by type" % story.type
    cur.execute(sql)
    print weblib.selectBox("type", cur.fetchall())


    print 'area:'
    cur = dbc.cursor()
    sql = "SELECT area, area, area='%s' from plan_area order by area" % story.area
    cur.execute(sql)
    print weblib.selectBox("area", cur.fetchall())

    print 'target:'
    cur = dbc.cursor()
    sql = "SELECT target, target, target='%s' from plan_target order by target" \
          % story.target
    cur.execute(sql)
    print weblib.selectBox("target", cur.fetchall())

    print 'status:'
    cur = dbc.cursor()
    sql = "SELECT status, status, status='%s' from plan_status order by status" \
          % story.status
    cur.execute(sql)
    print weblib.selectBox("status", cur.fetchall())
    print '<br>'


    print "summary:<br>" + \
          '<input type="text" name="summary" size="50" value="%s"><br>' \
          % story.summary

    print 'detail:<br>'
    print '<textarea cols="50" rows="5" name="detail">'
    print '%s</textarea><br>' % story.detail

    print "<b>risk/worth (1-10, 10 is most)</b><br>"
    print "risk:" + \
          '<input type="text" name="risk" size="5" value="%s">' \
          % weblib.deNone(story.risk)
    print "worth:" + \
          '<input type="text" name="worth" size="5" value="%s">' \
          % weblib.deNone(story.worth)

    print '<br>'
    print "<b>time estimates (in hours):</b><br>"
    print "Original:" + \
          '<input type="text" name="hrsOrig" size="5" value="%s">' \
          % weblib.deNone(story.hrsOrig)
    print "Current:" + \
          '<input type="text" name="hrsCurr" size="5" value="%s">' \
          % weblib.deNone(story.hrsCurr)
    print "Elapsed:" + \
          '<input type="text" name="hrsElapsed" size="5" value="%s">' \
          % weblib.deNone(story.hrsElapsed)

    print '<br>'
    print '<input name="action" value="save" type="submit">'
    print '</form>'




def showTotals(totals):
    
    print '<tr><td colspan="2" align="right">total:</td>'
    print '<td align="right">%s</td>' % totals['hrsOrig']
    print '<td align="right">%s</td>' % totals['hrsCurr']
    print '<td align="right">%s</td>' % totals['hrsElapsed']
    print '<td align="right">%.2f</td>' % totals['hrsRemain']
    print '</tr>'


def showStoryLinks():
    cur = dbc.cursor()
    cur.execute(
        """
        SELECT ID, area, summary, type, hrsOrig, hrsCurr, hrsElapsed, target, status,
               status in ('live', 'problem') as isLive
        FROM plan_story 
        WHERE status not in ('ignore', 'approved', 'duplicate')
        ORDER BY isLive DESC, target
        """)


    print weblib.trim(
        """
        <table width="100%" cellspacing="1"><tr>
        <th width="50">area</th>
        <th width="*">summary</th>
        <th width="50">Original</th>
        <th width="50">Current</th>
        <th width="50">Elapsed</th>
        <th width="50">Remain</th></tr>
        """)
    
    lastTarget = None
    totals = {}
    
    for row in cur.fetchall():
        
        (ID, area, summary, type,
         hrsOrig, hrsCurr, hrsElapsed,
         target, status, isLive) = row

        if isLive:
            target = "live"

        if target != lastTarget:
            if totals.keys():
                showTotals(totals)
    
            print '<tr><th style="background: #999999; text-align: left;"'
            print 'colspan="6">%s</th></tr>' % target

            lastTarget=target
            totals = {}


        if hrsCurr is None: hrsCurr = 0
        if hrsElapsed is None: hrsElapsed = 0
        hrsRemain = float(hrsCurr) - float(hrsElapsed)

        if float(hrsOrig) <= 0:
            type = "new"
        elif hrsRemain <= 0:
            type = "done"

        if status == 'problem':
            type = 'bug'

        totals['hrsOrig'] = totals.get('hrsOrig',0) + float(hrsOrig)
        totals['hrsCurr'] = totals.get('hrsCurr', 0) + float(hrsCurr)
        totals['hrsElapsed'] = totals.get('hrsElapsed', 0) + float(hrsElapsed)
        totals['hrsRemain'] = totals.get('hrsRemain', 0) + float(hrsRemain)

        print '<tr>'
        print '<td class="%s">%s</td>' % (type, area)
        print '<td class="%s"><a href="plan.py?ID=%s">%s</a></td>' % (type, ID, summary)
        print '<td class="%s" align="right">%s</td>' % (type, hrsOrig)
        print '<td class="%s" align="right">%s</td>' % (type, hrsCurr)
        print '<td class="%s" align="right">%s</td>' % (type, hrsElapsed)
        print '<td class="%s" align="right">%.2f</td>' % (type, hrsRemain)
        print '</tr>'

    showTotals(totals)
    print '</table>'


if __name__=="__main__":

    print weblib.trim(
        """
        <html>
        <title>zikeplan</title>
        <style class="text/css">
        body, td, th { font-size: 10pt; font-family: verdana }
        th { background: black; color:white; text-align: left; }
        .new {background: #66ff66; }
        .story { background: #ffcc66; }
        .bug { background: #ff6666; }
        .change { background: #33ccff; }
        .done {background: #cccccc; }
        </style>
        </html>
        """)

    print "<h1>zikeplan</h1>"

    if weblib.request.get("action"):
        weblib.auth.check()

    ed = zikebase.ObjectEditor(Story, weblib.request.get("ID"))
    ed.act()

    print '<b><a href="plan.py">add new</a></b><br>'
    print '<table><tr><td style="background: #cccccc">'
    showForm(ed.object)
    print '</td></tr></table>'

    print '<hr>'
    print 'KEY:'
    for tab in ('new', 'story', 'bug', 'change', 'done'):
        print '<span class="%s">&nbsp;%s&nbsp;</span>' % (tab,tab)

    print '<hr>'
    showStoryLinks()
    print '<hr>'

