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
# v0.2 1124.1999 sabren@manifestation.com
#      added o2x for emacs outline mode
#      seperated <zebra> and <report> tags
#      added if/el/code/exec/ etc..
#      (still alpha.. broke the compiler)
#
# v0.1 1017.1999 sabren@manifestation.com
#      initial version. (alpha release)
#
###################################################
##[ configuration ]################################
###################################################

#@TODO: python 1.5.2 has a new version of xmllib
import xmllib, re, string, types, o2x, sys

## useMessy allows us to write ill-formed XML so we don't
## have to litter our html with &lt; and &gt; entities
## @TODO: this should be part of the engine
useMessy = 0

###################################################
##[ zebra.Engine ]#################################
###################################################

class Engine (xmllib.XMLParser):
	reZVar = re.compile("{([$!]?\w+)}", re.I | re.S )

	###############################################

	def reset(self):

		"""Resets internal variables.
		called by XMLParser.__init__ and ZebraParser.parse"""
		
		xmllib.XMLParser.reset(self) # initiate base class

		# there's a .stack internal to XMLParser, but it's semi-protected,
		# and it changed from python 1.5.1 to 1.5.2 ... so I'm implementing
		# my own.. Start with None because "zebra" tag has no parent
		self.tagstack = [None]

		# datstack is a stack of various thingies (stripes/structures)
		self.datstack = []
	
		self.named  = {} # named structures go in here
		self.suits  = {} # suits go in here
		
		self.struct = {} # current structure (report, suit, etc)
		self.stripe = [] # current stripe

	###############################################

	def interpolate(self, match):

		"""replaces {fields}, {$vars} and {!slots}
		in a flattened zebra stripeset..."""

		#@TODO: this is all hard-coded for PHP3. make it generic.
		# @TODO: interpolation needs to be table driven so that
		# we can translate into different languages
		# (or maybe an overridable function?)
		# also, it ought to be per-stripe (and only used on stripe bodies and conditionals)
		# .. that way, we can change interpolation as context changes.

		token = match.group(1)
		if token[0]=="!":
			if self.zbr["named"].has_key(token[1:]):
				#return self.flatten(self.zbr["named"][token[1:]])
				return self.zbr["named"][token[1:]]
			else:
				return ""
		elif token[0] == "$":
			return token
		else:
			# fields.. there needs to be a standard
			# way of doing this per language.
			return '$__tr[' + token + ']';
		
	

	###############################################

	def handle_data(self, data):

		"""this method always adds text to the current stripe,
		because data can only occur within a stripe.."""

		if not string.strip(data):
			return
		elif (len(self.stripe) == 0) \
		or (type(self.stripe[-1])!=types.StringType):
			## time to add a new string to the list
			self.stripe.append(data)
		else:
			## rather than append, just merge it
			## with the existing string.
			self.stripe[-1] = self.stripe[-1] + data

	###############################################

	def unknown_starttag(self, tag, attrs):

		tag = string.replace (tag, "z:", "")
		self.tagstack.append(tag)

		if tag == "zebra":
			## @TODO: handle language attribute..
			pass
		elif tag == "report":
			self.datstack.append(self.struct)
			self.struct = {
				"tag"  : tag,
				"query": [],
				"head" : [],
				"body" : [],
				"tail" : [],
				"none" : [],
				"grouph": [], # group heads
				"groupt": [], # group tails
				"groups": [], # groups (fields)
				"gdepth": 0}  # group depth
		elif tag in ["query", "head", "body", "tail", "none"]:
			## then start a new stripe!
			self.datstack.append(self.stripe)
			self.stripe = []
			## @TODO: fix this:
			if tag=="query":
				self.struct["source"]=attrs["source"]
		elif tag in ["stripe", "show", "exec", "if", "el", "ef"]:
			## these are all special stripes with predefined properties
			if tag=="stripe" and attrs.has_key("name"):
				## start a new stripe stored in the "named" hash
				self.datstack.append(self.stripe)
				self.stripe = []
				self.named[attrs["name"]] = self.stripe
			else:
				## @TODO: there ought to be a stack for context..
				## @TODO: maybe these should be handled seperately?
				## @TODO: maybe this should all be generic code,
				## and only fiddled with in compile().. :)
				newStripe = {
					"tag"         : "stripe",
					"content"     : [],
					"context"     : "show",
					"conditional" : "do",
					"test"        : ""}
				## each type of stripe has defaults:
				if tag == "exec" : newStripe["context"] = "exec"
				if tag in ["if", "el", "ef"] : newStripe["conditional"] = tag
				## stripes let you override those things..
				for key in newStripe.keys():
					if attrs.has_key(key):
						newStripe[key] = attrs[key]
				self.stripe.append(newStripe)
				self.datstack.append(self.stripe)
				self.stripe = newStripe["content"]
		elif tag in ["title", "keywords", "description", "content"]:
			## these are just "named" stripes with predefined names
			self.datstack.append(self.stripe)
			self.stripe = []
			self.named[tag] = self.stripe
		elif tag == "group":
			self.struct["gdepth"] = self.struct["gdepth"] + 1
			if attrs.has_key("field"):
				self.struct["groups"].append(attrs["field"])
			else:
				pass
				## @TODO: only allow/require this for species
				#self.struct["groups"].append(None)
		else:
			pass # <zebra>, or unknown tag


	###############################################

	def unknown_endtag(self, tag):

		tag = string.replace (tag, "z:", "")
		self.tagstack = self.tagstack[:-1]
		parent = self.tagstack[-1]
		
		if tag in ["query", "head", "tail", "body", "none"]:
			if parent == "group" and tag in ["head", "tail"]:
				## grouph will look like: [outer, middle, inner]
				## groupt will look like: [inner, middle, outer]
				## It's just easier that way.
				self.struct["group" + tag[0]].append( self.stripe )
			else:
				self.struct[tag] = self.stripe
			self.stripe = self.datstack[-1]
			self.datstack = self.datstack[:-1]
		elif tag in ["report","suit"]:
			## append the structure to the current stripe
			self.stripe.append(self.struct)
			self.struct = self.datstack[-1]
		elif tag in ["stripe", "description", "content", "keywords", "show", "exec", "if", "el", "ef"]:
			## all we have to do is shift our attention to the
			## parent.. the current stripe is already a part of
			## the parent..
			self.stripe = self.datstack[-1]
			self.datstack = self.datstack[:-1]
		elif tag == "group":
			## not all groups have heads or tails. If this one
			## doesn't, even out the stack(s) with an empty value
			if len(self.struct["grouph"]) < len(self.struct["groups"]):
				self.struct["grouph"].append(None)
			## Remember, groupt is in backwards order from
			## grouph. It sounds strange, but that actually is what I want,
			## because that's the order in which I'll need them.
			## so, grouph and groupt get processed the same here.
			if len(self.struct["groupt"]) < len(self.struct["groups"]):
				self.struct["groupt"].append(None)
		else:
			pass # </zebra>, or unknown tag


	###############################################

	def parse(self, zbr):

		self.reset()
		self.feed(zbr)
		self.close
		return {"stripe" : self.stripe,
				"named"  : self.named,
				"suits"  : self.suits,}

	###############################################

	def flatten_report(self, report, depth=0):

		# @TODO: this is one serious kludge.
		# @TODO: code each variable name with depth so can have nested reports
		res = ""
		res = res + \
			  "$__db = new " + report["source"] + ";\n" + \
			  "$__db->query(\"" + self.flatten(report["query"]) + "\");\n"

		## set up two arrays for handling groups
		res = res + "$__groups=array('all'"
		buf = "$__showtail=array(0"
		for g in report["groups"]:
			res = res + ", '" + g + "'"
			buf = buf + ",0"
		res = res + ");\n"
		res = res + buf + ");\n"

		## now do the test:
		res = res + "if ($__db->next_record()) {\n";

		## if there's records, show the head:
		res = res + "   " + self.flatten(report["head"],depth,"show")

		## nr is next record, tr = this one, pr = previous
		## we need to look at 3 records at once in order to 
		## know when to print the headers and footers..
		res = res + \
			  "   $__nr = $__db->Record;\n" + \
			  "   while (($__more = $__db->next_record()) or (! $__nomore)){\n" + \
			  "      $__tr = $__nr;\n" + \
			  "      if ($__more) { $__nr = $__db->Record; }\n" + \
			  "      else { $__nomore = 1; }\n"

		## handle the grouping for the heads:
		for i in range(len(report["groups"])):
			if report["grouph"][i]:
				res = res + \
					  "      if ($__nr[\"" + report["groups"][i] + "\"] != $__pr[\"" + \
					  report["groups"][i] + "\"]){\n" + \
					  "         " + self.flatten(report["grouph"][i],depth,"show") + \
					  "         unset($__pr);\n" + \
					  "      }\n"
				
		## now the body:
		res = res + "      " + self.flatten(report["body"],depth,"show")

		## and the tails:
		## .. use a while loop because they're faster than for loops in php3
		res = res + \
			  "      if ($__nomore) { $__showTail[0] = 1; }\n" + \
			  "      $__g=1; while ($__g < sizeof($__showTail)){ \n" + \
			  "         if (($__nr[$__groups[$__g]] != $__tr[$__groups[$__g]]) " + \
			  "or ($__showTail[$__g-1])){\n" + \
			  "            $__showTail[$__g] = 1;\n" + \
			  "         } else {\n" + \
			  "            $__showTail[$__g] = 0;\n" + \
			  "         }\n" + \
			  "         $__g++;\n" + \
			  "      }\n"

		for i in range(len(report["groups"])):
			if report["groupt"][i]:
				res = res + \
					  "      if ($__showTail[" + `i+1` + "]){\n" + \
					  "         " + self.flatten(report["groupt"][i],depth,"show") + \
					  "      }\n"

		## cap off the loop, show the tail...
		res = res + \
			  "      $__pr = $__tr;\n" + \
			  "   }\n" + \
			  "   " + self.flatten(report["tail"],depth,"show")

		## handle "none"
		if report["none"]:
			res = res + \
				  "} else {\n" + \
				  self.flatten(report["none"],depth,"show")
		res = res + "}\n"

		## finally, encode variables with depth, so we can nest reports
		reDepth = re.compile("(\$__\w+)", re.I | re.S )
		res = reDepth.sub(r"\1_" + `depth`,res)

		return res



	###############################################

	def flatten(self, stripeset, depth=0, context="exec"):

		"""Converts a stripe or stripeset into a string"""

		res = ""
		if type(stripeset)!=types.ListType:
			stripeset = [stripeset]

		for stripe in stripeset:
			stripehead  = stripebody  = stripetail  = ""
			test = conditional = ""
			if type(stripe)==types.StringType:
				## strip leading and trailing newlines
				if stripe[1] == "\n": 
					stripe = stripe[1:]
				if stripe[-1] == "\n":
					stripe = stripe[:-1]
				## deal with context (we only care when it's a string)
				if (context == "show"):
					stripehead = 'print "'
					stripebody = string.replace(stripe, '"', '\\"')
					stripetail = '";'
				elif context == "exec":
					stripebody = stripe
				else:
					#@TODO: this should raise an error
					pass
			elif type(stripe)==types.ListType:
				stripebody = self.flatten(stripe,depth+1)
			elif type(stripe)==types.DictionaryType:
				# @TODO: this ought to all be stored in a
				# dictionary mapping tags to functions
				tag = stripe["tag"]
				if tag == "stripe":
					stripebody = self.flatten(stripe["content"],depth+1,
											  stripe["context"])[:-1]
					test   = stripe["test"]
					conditional = stripe["conditional"]
				elif tag == "report":
					res = res + self.flatten_report(stripe, depth+1)
				else:
					print "*** don't know how to flatten " + tag
			else:
				raise("unknown structure in stripe")
			
			## finally, the conditional
			if (test) and not (conditional):
				conditional = "if"
			if (test) or (conditional): # el has no condition
				conditionals = {"if":"if", "ef":"elseif", "el":"else"}
				if conditional == "":
					conditional = "if"
				if conditional in ["if", "ef"]:
					stripehead = conditionals[conditional] + " (" \
								 + test + "){\n" \
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

	###############################################

	def compile(self, xml):

		return "<?\n" + self.flatten(self.parse(xml)) + "?>"


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

if __name__ == "__main__":

	if len (sys.argv) > 1:
		zbo = open(sys.argv[1]).read()
	else:
		zbo = sys.stdin.read()

	## convert outline mode to XML:
	xml = o2x.o2x(zbo)

	## convert XML into python:
	zEngine = Engine()

	#print zEngine.compile(xml)
	print zEngine.parse(xml)
