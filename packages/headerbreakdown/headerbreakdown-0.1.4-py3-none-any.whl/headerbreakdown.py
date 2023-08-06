import json

class HeaderBreakdown:
	def __init__(self, headers):
		''' initialize the object and set output attributes to None, to be populated later by process() '''
		self.headers = headers
		self.direction = None
		self.http_version = None
		self.method = None
		self.host = None
		self.path = None
		self.user_agent = None
		self.response_code = None
		self.response_phrase = None
		self.summary = None
		self.output = None
		self.json = None
		self.nested_output = None
		self.nested_json = None
		self.nested_direction_output = None
		self.nested_direction_json = None
		self.notices = []
		# have class methods run when the object is initialized
		self.process()

	def dgen(self, d, k, v):
		''' nested dictionary builder '''
		if k not in d.keys():
			d.setdefault(k,[])
			d[k].append(v)
		elif k in d.keys():
			d[k].append(v)

	def identifyMicrovalues(self, v):
		''' identify micro key/value pairs, using an equal sign, inside a header value '''
		d = {}
		if "=" in v:
			z = [i.strip().replace("'","").replace('"','') for i in v.split("=")]
			d["microkey"] = z[0]
			d["microvalue"] = z[1]
			return(d)

	def identifyMinivalues(self, v):
		''' identify mini key/value pairs, using a comma, inside a header value '''
		d = {}
		if "," in v:
			z = list(set([i.strip().replace("'","").replace('"','') for i in v.split(",")]))
			d["minivalues"] = z
			return(d)

	def identifySubvalues(self, v):
		''' identify sub key/value pairs, using a semicolon OR comma if semicolon is not present, inside a header value '''
		d = {}
		# semicolon, or comma without semicolon, determines subvalues
		if ";" in v:
			z = list(set([i.strip().replace("'","").replace('"','') for i in v.split(";")]))
			d["subvalues"] = z
		elif "," in v and ";" not in v:
			z = list(set([i.strip().replace("'","").replace('"','') for i in v.split(",")]))
			d["subvalues"] = z
		# attempt to identify links inside angle brackets
		if "subvalues" in d:
			ll = []
			for i in d["subvalues"]:
				if "<" in i and ">" in i:
					l = i.split("<")[1].split(">")[0].strip()
					ll.append(l)
			if len(ll) > 0:
				d["subvalue-found-links"] = list(set(ll))
		return(d)

	def processHeaders(self, h):
		''' identify direction, a few common header values, and begin processing header values '''
		d = {}
		for i in h:
			if "HTTP/" in i:
				x = i.split()
				if len(x) == 3:
					if "HTTP/" in x[0]:
						self.direction = "response"
						self.http_version = x[0]
						self.response_code = x[1]
						x[2] = " ".join(x[2:]).strip()
						self.response_phrase = x[2]
						d["direction"] = "response"
						d["http_version"] = x[0]
						d["response_code"] = x[1]
						d["response_phrase"] = x[2]
					elif "HTTP/" in x[2]:
						self.direction = "request"
						self.method = x[0]
						self.path = x[1]
						self.http_version = x[2]
						d["direction"] = "request"
						d["method"] = x[0]
						d["path"] = x[1]
						d["http_version"] = x[2]
			if ":" in i:
				x = i.split(":")
				x[1] = ":".join(x[1:]).strip()
				x = [x[0], x[1]]
				if x[0] in d:
					self.notices.append("duplicated_header::{}".format(x[0]))
				self.dgen(d, x[0], x[1])
				if x[0] == "Host":
					if "host" not in d:
						d["host"] = x[1]
						self.host = x[1]
				elif x[0] == "User-Agent":
					if "user_agent" not in d:
						d["user_agent"] = x[1]
						self.user_agent = x[1]
		#
		#
		# clean the dictionary
		# combine all instances of duplicated cookies into one item
		ll = []
		if "Set-Cookie" in d:
			for i in d["Set-Cookie"]:
				ll.extend(i)
			d["Set-Cookie"] = ["".join(ll)]
		#
		#
		# simple header breakdowns for later analysis
		#
		#
		# ensure all values are unique, then convert to a string as subkey "value"
		for k,v in d.items():
			# do not alter hard-set items
			ntk = ["direction", "response_code", "response_phrase", "method", "path", "host", "user_agent", "http_version", "multiple_hosts_detected"]
			if k not in ntk:
				d[k] = {"key":k, "value":"".join(list(set(v)))}
				v = d[k]["value"]
		#
		#
		# perform subvalue identification here
		for k,v in d.items():
			if "value" in v:
				# in this case, v is the header-as-a-dict-key, so v[value] is the actual header content
				if "=" in v["value"]:
					v["microvalues"] = {}
				sv = self.identifySubvalues(v["value"])
				if len(sv) > 0:
					v["subvalues"] = sv["subvalues"]
					if "subvalue-found-links" in sv:
						v["subvalue-found-links"] = list(set(sv["subvalue-found-links"]))
					for i in sv["subvalues"]:
						if "," in i:
							mv = self.identifyMinivalues(v)
							if mv is not None:
								if len(mv) > 0:
									self.dgen(v["minivalues"], cv["minikey"], cv["minivalue"])
						if "=" in i:
							cv = self.identifyMicrovalues(i)
							if len(cv) > 0:
								self.dgen(v["microvalues"], cv["microkey"], cv["microvalue"])
						# note that something like "Location: https://www.google.com/?gws_rd=ssl" would not produce microvalues
		#
		#
		# simple arrays of unique header keys and values for easier top-level queries
		keys = []
		values = []
		for k,v in d.items():
			if "value" in v:
				keys.append(d[k]["key"])
				values.append(d[k]["value"])
		keys = list(set(keys))
		values = list(set([i.strip().replace("'","").replace('"','') for i in values]))
		if len(keys) > 0 and len(values) > 0:
			d["keys"] = keys
			d["values"] = values
		#
		#
		# simple arrays of unique microkeys/microvalues for easier top-level queries
		microkeys = []
		microvalues = []
		for k,v in d.items():
			if "microvalues" in v:
				if len(v["microvalues"]) == 0:
					v.pop("microvalues", None)
				else:
					for kk,vv in v["microvalues"].items():
						microkeys.append(kk)
						microvalues.extend(vv)
		microkeys = list(set(microkeys))
		microvalues = list(set(microvalues))
		if len(microkeys) > 0 and len(microvalues) > 0:
			d["microkeys"] = microkeys
			d["microvalues"] = microvalues
		#
		#
		# simple arrays of links found in angle brackets for easier top-level queries
		sfl = []
		for k,v in d.items():
			if "subvalue-found-links" in v:
				sfl.extend(v["subvalue-found-links"])
		if len(sfl) > 0:
			sfl = list(set(sfl))
			d["subvalue-found-links"] = sfl
		#
		#
		# additional notices
		#
		#
		# flatten the multiple_hosts_detected list-of-lists into a single list
		if "multiple_hosts_detected" in d:
			self.notices.append("multiple_hosts_detected")
			d["multiple_hosts_detected"] = [h[0] for h in d["multiple_hosts_detected"]]
		#
		#
		# count "dots" in host fields
		if "Host" in d:
			d["host_dot_count"] = d["Host"]["value"].count(".")
			d["host_dot_count_true"] = d["host"].count(".")
			if d["host_dot_count"] != d["host_dot_count_true"]:
				self.notices.append("host_dot_count_mismatch")
		#
		#
		# return a dictionary
		return(d)

	def splitHeaders(self, line):
		''' splits a string of headers into a list '''
		h = line.split("\r\n\r\n")[0]
		hh = h.split("\r\n")
		#d = {"headers":self.processHeaders(hh)}
		d = self.processHeaders(hh) # dictionary
		return(d)

	def process(self):
		''' primary method which initiates the main actions and returns a dictionary, but also sets self.output and self.json '''
		h = self.splitHeaders(self.headers)
		if len(self.notices) > 0:
			self.notices = list(set(self.notices))
			h["notices"] = self.notices
		self.output = h
		self.json = json.dumps(h)
		# *_nested just places the returned dictionary as self-contained value for top-level key "headers"
		self.nested_output = {'headers':h}
		self.nested_json = json.dumps(self.nested_output)
		# *_nested_direction places the returned dictionary further down under headers --> request or response key
		if self.direction is not None:
			self.nested_direction_output = {'headers':{str(self.direction):h}}
			self.nested_direction_json = json.dumps(self.nested_direction_output)
		#
		#
		#
		# create string for self.summary and __repr__()
		s = ""
		s += "\\"*100+"\n"
		s += self.json+"\n"
		s += "~"*100+"\n"
		if self.direction is not None:
			s += "direction\t"+self.direction+"\n"
		if self.http_version is not None:
			s += "http_version\t"+self.http_version+"\n"
		if self.method is not None:
			s += "method\t\t"+self.method+"\n"
		if self.host is not None:
			s += "host\t\t"+self.host+"\n"
		if self.path is not None:
			s += "path\t\t"+self.path+"\n"
		if self.user_agent is not None:
			s += "user_agent\t"+self.user_agent+"\n"
		if self.response_code is not None:
			s += "response_code\t"+self.response_code+"\n"
		if self.response_phrase is not None:
			s += "response_phrase\t"+self.response_phrase+"\n"
		if self.notices is not None:
			if len(self.notices) > 0:
				s += "notices\t\t"+" | ".join(self.notices)+"\n"
		s += "/"*100
		self.summary = s
		#
		#
		#
		return(h)

	def __repr__(self):
		''' returns a large string of output data for on-screen viewing '''
		return(self.summary)