from multiprocessing import Pool
import requests

CHUNKSIZE = 1024 * 1024

class Downloader:
	def __init__(self, config, servers, users, downloads):
		self.servers = servers
		self.users = users
		self.downloads = downloads
		self.download_folder = config["download_folder"]

	def start(self, servername, filename, user):
		
		if self.servers.protocol(servername) == "http":

			### get file headers
			url = self.servers.url(servername, filename)
			headers = self.servers.headers(servername)

			res = requests.head(url, headers=headers)

			### if not exist, mark error
			if res.status_code != 200: 
				print "error: ", res.status_code, filename
				self.downloads.update_error(filename, servername)
				return

			### create before multiple writes
			filepath = self.download_folder + filename
			with open(filepath, "wb") as fd:
				pass

			print "Downloading", filename, "from server", servername, "to", filepath

			### count and distribute chunk tasks
			nbytes = int(res.headers["content-length"])
			chunks = [{"start": i, "end": min(i+CHUNKSIZE, nbytes-1), "url":url, "filepath": filepath, "headers": headers}  for i in range(0, nbytes, CHUNKSIZE)]

			workers = Pool(4)
			workers.map(download_chunk, chunks)

def download_chunk(data):
	try:
		start = data["start"]; end = data["end"]
		headers = data["headers"]; filepath = data["filepath"]; url = data["url"]

		### add range headers and get the chunk
		headers["Range"] = 'bytes=%s-%s' % (start, end)
		res = requests.get(url, headers=headers)

		### write to file, use r+b to avoid clearing all content
		with open(filepath, "r+b") as fd:
			fd.seek(start)
			fd.write(res.content)

		return True
	except Exception as err:
		print err
		return False
