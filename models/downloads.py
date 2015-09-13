from models import Model, enum, timestamp
from tinydb import where
from datetime import datetime

"""
	SCHEMA
	{
		"filename": the filename
		"server": the server name or full download url (including filename)
		"size": (estimated) file size in bytes
		"known": whether the server is a known server (included in preconfig) or not (thus full url)
		"status": Status enum
		"queuetime": queue timestamp
		"starttime": start timestamp
		"endtime": finished / error timestamp
		"user": proxy account used for downloading
	}
"""

Status = enum(
	QUEUE = 0,
	DOWNLOADING = 1,
	FINISHED = 2,
	ERROR = -1
)

class Downloads(Model):
	def __init__(self, dbpath):
		Model.__init__(self, dbpath, "downloads")
		self.Status = Status

	def insert(self, filename, server, size):
		return self.db.insert({"filename": filename, "server": server, "size": size, "known": True, "status": Status.QUEUE, "queuetime": timestamp()})

	def insertUrl(self, filename, url, size):
		return self.db.insert({"filename": filename, "server": url, "size": size, "known": False, "status": Status.QUEUE, "queuetime": timestamp()})

	def get_queue(self):
		return self.db.search(where("status") == Status.QUEUE)

	def get_download(self):
		return self.db.search(where("status") == Status.DOWNLOADING)

	def get_finish(self):
		return self.db.search(where("status") == Status.FINISHED)

	def update_download(self, filename, server, user):
		self.db.update({"status": Status.DOWNLOADING, "starttime": timestamp(), "user": user}, (where("filename") == filename) & (where("server") == server))

	def update_error(self, filename, server):
		self.db.update({"status": Status.ERROR, "endtime": timestamp()}, (where("filename") == filename) & (where("server") == server))

	def update_finish(self, filename, server):
		self.db.update({"status": Status.FINISHED, "endtime": timestamp()}, (where("filename") == filename) & (where("server") == server))

	def delete(self, filename, server):
		self.db.remove((where("filename") == filename) & (where("server") == server))