###################################################
# zebra.py
#
#	python implementation of zebra,
#	an XML-based template engine and code
#   generator
#
#   This code is free and may be redistributed
#   or copied under the terms of the GNU General
#   Public License. See http://www.fsf.org/ for details
#
# v0.1a 1017.1999 sabren@manifestation.com
#       initial version. (alpha release)
#
###################################################
##[ configuration ]################################
###################################################

#@TODO: python 1.5.2 has a new version of xmllib
import xmllib, re, string, types, o2x

## useMessy allows us to write ill-formed XML so we don't
## have to litter our html with &lt; and &gt; entities
useMessy = 1

zbr = open("test/striped.zbr", "r").read()
#zbr = open("blogsearch.zbr", "r").read()
spc = open("test/empty.spc", "r").read()
#spc = open("viewpage.spc", "r").read()
#zbo = open("test/example.zbo", "r").read()

#zbr = open("test_report.zbr", "r").read()
#spc = open("test_species.zbr", "r").read()

###################################################
##[ ZebraParser ]##################################
###################################################

class ZebraParser(xmllib.XMLParser):

	def reset(self):
		"""Resets internal variables.
		called by XMLParser.__init__ and ZebraParser.parse"""
		
		xmllib.XMLParser.reset(self) # initiate base class
		self.struct  = {
			"named": {}, "groups": [], "grouph": [], "groupt": [],
			"query": None, "head": None, "body": None, "tail": None }
		self.aStripe = []
		self.stripes = []
		self.gdepth  = 0


	def handle_data(self, data):
		"""this method always adds text to the current stripe,
		because data can only occur within a stripe.."""
		#data = string.strip(data)
		if not string.strip(data):
			return
		elif (len(self.aStripe) == 0) \
		or (type(self.aStripe[len(self.aStripe)-1])!=types.StringType):
			## time to add a new string to the list
			self.aStripe.append(data)
		else:
			## rather than append, just merge it
			## with the existing string.
			self.aStripe[len(self.aStripe)-1] = \
			self.aStripe[len(self.aStripe)-1] + data


	def unknown_starttag(self, tag, attrs):
		tag = string.replace (tag, "z:", "")
		if tag in ["body", "head", "tail", "query"]:
			## then start a new stripe!
			self.stripes.append(self.aStripe)
			self.aStripe = []
			if tag=="query":
				self.struct["query_source"]=attrs["source"]
		elif tag in ["stripe", "named"]:
			## same as above, but account for attribs
			newStripe = {
				"content"     : [],
				"context"     : "show",
				"conditional" : "do",
				"condition"   : ""}
			for key in newStripe.keys():
				if attrs.has_key(key):
					newStripe[key] = attrs[key]
			self.aStripe.append(newStripe)
			self.stripes.append(self.aStripe)
			self.aStripe = newStripe["content"]
			if tag=="named":
				#@TODO: named inside anything else should error
				self.struct["named"][attrs["name"]] = [newStripe]
		elif tag == "group":
			self.gdepth = self.gdepth + 1
			if attrs.has_key("field"):
				self.struct["groups"].append(attrs["field"])
			else:
				pass
				## @TODO: only allow/require this for species
				#self.struct["groups"].append(None)
		else:
			pass # <zebra>, or unknown tag


	def unknown_endtag(self, tag):
		parent = self.stack[len(self.stack)-2]
		parent = string.replace (parent, "z:", "")
		tag = string.replace (tag, "z:", "")
		if tag in ["head", "tail", "query"]:
			if parent == "zebra":
				self.struct[tag] = self.aStripe
			elif parent == "group":
				## grouph will look like: [outer, middle, inner]
				## groupt will look like: [inner, middle, outer]
				## It's just easier that way.
				self.struct["group" + tag[0]].append( self.aStripe )
			self.aStripe = []
		elif tag == "body":
			self.struct["body"] = self.aStripe
			self.aStripe = []
		elif tag in ["stripe", "named"]:
			## all we have to do is shift our attention to the
			## parent.. the current stripe is already a part of
			## the parent..
			self.aStripe = self.stripes[len(self.stripes)-1]
			self.stripes = self.stripes[:-1]
		elif tag == "group":
			## not all groups have heads or tails. If this one
			## doesn't, even out the stack(s) with an empty value
			if len(self.struct["grouph"]) < len(self.struct["groups"]):
				self.struct["grouph"].append(None)
			## Remember, groupt is in backwards order from
			## grouph. It sounds strange, but that actually is what I want,
			## because that's the order in which I'll need them.
			## so, grouph and groupt get processed the same here.
			if len(self.struct["groupt"]) \
			   < len(self.struct["groups"])-self.gdepth:
				self.struct["groupt"].append(None)
		else:
			pass # </zebra>, or unknown tag


	def parse(self, zbr):
		self.reset()
		self.feed(zbr)
		self.close

		#@TODO: fix this. it's just a hack specific to PHP3
		res = ", "
		for g in self.struct["groups"]:
			res = res + "'" + g + "'" + ', '
		res=res[0:-2] # strip last comma & space
		self.struct["group_list"] = res
		return self.struct


###################################################
##[ ZebraCompiler ]################################
###################################################

class ZebraCompiler:
	zbr = {}
	spc = {}
	reZVar = re.compile("{[$]?(z:|n:)?\w+}", re.I | re.S )

	def interpolate(self, match):
		"""replaces {fields}, {$vars} and {$z:zebravars}
		in a flattened zebra stripeset..."""

		#@TODO: this is all hard-coded for PHP3. make it generic.
		token = match.group(0)
		if token[1:4]=="$z:":
			return self.zbr[token[4:-1]]
		if token[1:4]=="$n:":
			if self.zbr["named"].has_key(token[4:-1]):
				return self.zbr["named"][token[4:-1]]
				#return self.flatten(self.zbr["named"][token[4:-1]])
			else:
				return ""
		elif token[1] == "$":
			return token[1:-1] # strip the "}"
		else:
			return '$zrec[' + token[1:-1] + ']';

	
	def flatten(self, stripeset, depth=0, context="exec"):
		"""Converts a stripe or stripeset into a string"""
		
		res = ""
		if type(stripeset)!=types.ListType:
			stripeset = [stripeset]
			
		for stripe in stripeset:
			stripehead  = ""
			stripetail  = ""
			condition   = ""
			conditional = ""
			if type(stripe)==types.StringType:
				## deal with context (we only care when it's a string)
				if (context == "show"):
					stripehead = 'print "'
					stripebody = string.replace(stripe, '"', '\\"')
					stripetail = '";'
				elif context == "exec":
					stripebody = stripe
				else:
					#@TODO: this should give an error
					pass
			elif type(stripe)==types.ListType:
				stripebody = self.flatten(stripe,depth+1)
			elif type(stripe)==types.DictionaryType:
				stripebody = self.flatten(stripe["content"],depth+1,
										  stripe["context"])[:-1]
				condition   = stripe["condition"]
				conditional = stripe["conditional"]
			else:
				raise("unknown structure in stripe")
			
			## finally, the conditional
			if (condition) and not (conditional):
				conditional = "if"
			if (condition) or (conditional): # el has no condition
				conditionals = {"if":"if", "ef":"elseif", "el":"else"}
				if conditional == "":
					conditional = "if"
				if conditional in ["if", "ef"]:
					stripehead = conditionals[conditional] + " (" \
								 + condition + "){\n" \
								 + "   " + stripehead
					stripetail = stripetail + "\n}"
				elif conditional == "el":
					stripehead = conditionals[conditional] + " {" \
								 + "   " + stripehead
					stripetail = stripetail + "\n}"
					
			res = res + stripehead + stripebody + stripetail + "\n"

		# now that we have the whole set, interpolate variables:
		res = self.reZVar.sub(self.interpolate, res)
		return res

	
	def compile(self, zebra={}, species={} ):
		""" flatten zebra and species, merge them together"""
		
		self.zbr = zebra
		self.spc = species
		res = ""
		gtails = ""

		# first flatten the zebra
		self.zbr["query"] = self.flatten(self.zbr["query"])
		for part in ('head', 'body', 'tail'):
			self.zbr[part] = self.flatten(self.zbr[part],0,"show")
		for part in self.zbr["named"].keys():
			self.zbr["named"][part] = \
				 self.flatten(self.zbr["named"][part],0,"show")
		for i in range(len(self.zbr["grouph"])):
			self.zbr["grouph"][i] = \
				 self.flatten(self.zbr["grouph"][i],0,"show")
		for i in range(len(self.zbr["groupt"])):
			self.zbr["groupt"][i]=self.flatten(self.zbr["groupt"][i],0,"show")

		# now merge with the body
		if self.spc.has_key("head"):
			res = res + self.flatten(spc["head"],0)

		if self.spc.has_key("groups"):
			self.zbr["temphead"] = self.zbr["head"]
			self.zbr["temptail"] = self.zbr["tail"]
			gcount = len(self.zbr["groups"])
			for i in range(gcount):
				self.zbr["head"] = self.zbr["grouph"][i]
				self.zbr["tail"] = self.zbr["groupt"][gcount-i-1]
				self.zbr["group_depth"] = `i+1` # convert to string
				self.zbr["group_field"] = self.zbr["groups"][i]
				res = res + self.flatten(self.spc["grouph"][0])
				gtails = self.flatten(self.spc["groupt"][0]) + gtails
			self.zbr["head"] = self.zbr["temphead"]
			self.zbr["tail"] = self.zbr["temptail"]
			
		if self.spc.has_key("body"):
			res = res + self.flatten(self.spc["body"])
		else:
			# this accounts for species with no <body> tag
			res = res + "{$z:body}"
		if self.spc.has_key("groups"):
			res = res + gtails # defined above
		if self.spc.has_key("tail"):
			res = res + self.flatten(spc["tail"])
		print res

###################################################
## cleanup striped tags if useMessy is turned on ##
###################################################
## @TODO: account for freestanding <'s (eg, in a script)
## @TODO: *OR* account for <![CDATA[]]>
if (useMessy):
	reTag	= re.compile("(<)([^>]+)(>)", re.I | re.S )
	reClean = re.compile("[!?]|/?z:.*", re.I | re.S )

	def tidy(mess):
		if reClean.match(mess.group(2)):
			return mess.group(0)
		else:
			return "&lt;" + mess.group(2) + "&gt;"

	## so clean it up already:
	zbr = reTag.sub(tidy, zbr)


###################################################
##[ main code ]####################################
###################################################

## convert .XML's into python structures:
zParser = ZebraParser()
zbr = zParser.parse(zbr)
spc = zParser.parse(spc)

## now put the pieces together:
zCompiler = ZebraCompiler()
zCompiler.compile(zebra=zbr, species=spc)

##-end-##
