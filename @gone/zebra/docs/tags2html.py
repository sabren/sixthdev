import xmllib, o2x, re, time

class tagdoc(xmllib.XMLParser):

	def __init__(self):
		xmllib.XMLParser.__init__(self)
		self.STRIPE = "" # used to cache data between tags

	## main menu at the top:
	
	def start_group(self, attrs):
		print "<h3>" + attrs["name"] + "</h3>\n<ul>"

	def end_group(self):
		print "</ul>"

	def start_item(self, attrs):
		print '<li><a href="#%s">%s</a>' % (attrs["tag"], attrs["tag"])


	## individual tags
	def start_tag(self, attrs):
		print '<h2><a name="%s">%s</a></h2>' % (attrs["name"], attrs["name"])
		self.attriblist = []

	def end_tag(self):
		if len(self.attriblist) > 0:
			print """<table width="70%" border="1"><tr><th align="left">attribute</th><th align="left">meaning</th></tr>"""
			for a in self.attriblist:
				print "<tr><td>%s</td><td>%s</td></tr>" % (a["name"], a["desc"])
			print "</table>"
			

	def start_desc(self, attrs):
		self.STRIPE = ""
		print '<p class="desc">'

	def end_desc(self):
		print self.STRIPE
		print '</p>'

	def start_example(self, attrs):
		self.STRIPE = ""
		print '<pre class="example">'

	def end_example(self):
		print self.STRIPE
		print '</pre>'

	def start_attr(self, attrs):
		self.attriblist.append(attrs)

	def start_split(self, attrs):
		print "<hr>"

	## char data
	def replaceAts(self, match):
		tag = match.group(1)
		return '<a href="#%s">&lt;%s&gt;</a>' % (tag, tag)

	def handle_data(self, data):
		reAt = re.compile("\@\@([^@]+)\@\@", re.I | re.S )
		res = reAt.sub(self.replaceAts,data)
		self.STRIPE = self.STRIPE + res

print """
<html>
<head>
<title>Zebra Tag Reference</title>
<style type="text/css">
body, p, td, th {
  background: white;
  font-family: verdana, arial
  font-size: 10pt;
}

.desc, .example, table {
  margin-left: 25px;
  margin-right: 50px;
}

th { color: white; background: black }
td { color: black; background: #ccccff }

pre.example {
  background: gold;
}
</style>
</head>
<body>
<h1>Zebra Tag Reference</h1>
<p><b>last updated:</b> %s <br>
Zebra is in flux at the moment, so the documentation may
be slightly ahead of or behind the current code. They
should sync up around release 1.0.
</p>
<a href="../">back to main zebra page</a>
""" % time.asctime(time.localtime(time.time()))

docs = tagdoc()
docs.feed(o2x.o2x(open("tags.out").read()))

print """
<hr>
&copy; 1999 Zike Interactive.... <a href="../">back to main zebra page</a>
</body>
</html>
"""
