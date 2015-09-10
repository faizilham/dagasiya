from models import Model, enum, timestamp
from tinydb import where

"""
	SCHEMA
	{
		"filename": the filename
		"server_name": the server name
		"status": Status enum
		"timestamps": list of status change timestamps
		"user": proxy account used for downloading
	}
"""

Status = enum("QUEUE", "DOWNLOADING", "FINISHED")

def set_status(status):
	def transform(element):
		element.status = status
		element.timestamps.append(timestamp())

	return transform

class Downloads(Model):
	def __init__(self, dbpath):
		Model.__init__(self, dbpath, "downloads")
		self.Status = Status

	def insert(self, filename, server_name):
		return self.db.insert({"filename": filename, "server_name": server_name, "status": Status.QUEUE, "timestamps": [timestamp()]})

	def get_queue(self):
		return self.db.search(where("status") == Status.QUEUE)

	def get_download(self):
		return self.db.search(where("status") == Status.DOWNLOADING)

	def get_finish(self):
		return self.db.search(where("status") == Status.FINISHED)

	def update_download(self, filename, server_name, user):
		def set_download(element):
			set_status(Status.DOWNLOADING)(element)
			element.user = user

		self.db.update(set_download, (where("filename") == filename) & (where("server_name") == server_name))

	def update_finish(self, filename, server_name):
		self.db.update(set_status(Status.FINISHED), (where("filename") == filename) & (where("server_name") == server_name))

	def delete(self, filename, server_name):
		self.db.remove((where("filename") == filename) & (where(server_name) == server_name))