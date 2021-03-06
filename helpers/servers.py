import base64

class Proxy(object):
	def __init__(self, proxy_settings):
		self.protocol = proxy_settings["protocol"]
		self.proxy_template = "{protocol}://{{user}}:{{passwd}}@{host}:{port}".format(**proxy_settings)
		
	def url(self, user, passwd):
		return self.protocol, self.proxy_template.format(user=user, passwd=passwd)

class Servers(object):
	def __init__(self, servers):
		self.servers = servers

		for name in servers:
			server = servers[name]
			url, headers = self.create_urlheaders(server)
			server["url"] = url
			server["headers"] = headers

	def create_urlheaders(self, server):
		if (server["protocol"] == "ftp"):
			port = server["port"] if "port" in server else 21
			if ("passwd" in server):
				return "ftp://{user}:{passwd}@{host}:{port}{base_url}".format(
					user=server["user"],
					passwd=server["passwd"],
					host=server["host"],
					port=port,
					base_url=server["base_url"]
				), []
			else:
				return "ftp://{host}:{port}{base_url}".format(
					host=server["host"],
					port=port,
					base_url=server["base_url"]
				), []
		else: # http
			port = server["port"] if "port" in server else 80
			headers = {}

			if ("passwd" in server):
				base64string = base64.encodestring('%s:%s' % (server["user"], server["passwd"])).replace('\n', '')
				headers["Authorization"] = "Basic %s" % base64string

			return "http://{host}:{port}{base_url}".format(
				host=server["host"],
				port=port,
				base_url=server["base_url"]
			), headers

	def url(self, servername, filename):
		return self.servers[servername]["url"] + filename

	def headers(self, servername):
		return self.servers[servername]["headers"]

	def protocol(self, servername):
		return self.servers[servername]["protocol"]

	def __getitem__(self, key):
		return self.servers[key]