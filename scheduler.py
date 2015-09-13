from datetime import datetime
from threading import Thread
import bisect

class Scheduler(object):
	def __init__(self, config, downloads, users, downloader):
		self.downloads = downloads
		self.users = users
		self.free_time_start = config["free_time_start"]
		self.free_time_end = config["free_time_end"]
		self.downloader = downloader

	def free_time(self):
		current = datetime.now().time()
		return (self.free_time_start < current) and (current < self.free_time_end)

def get_available(e):
	return e["quota"] - e["usage"]

def download_from_server(downloader, filename, servername, username):
	downloader.start(filename, servername, username)

class SimpleScheduler(Scheduler):
	def __init__(self, config, downloads, users, downloader):
		Scheduler.__init__(self, config, downloads, users, downloader)

	def schedule(self):
		users = self.users.all()

		users.sort(key=get_available)
		queue = self.downloads.get_queue()

		jobs = []

		for download in queue:
			if download["size"] < get_available(users[0]):
				user = users.pop(0)

				if download["known"]:
					job = Thread(target=download_from_server, args=(self.downloader, download["filename"], download["servername"], user["name"]))
					job.start()
					jobs.append(job)
				else
					pass

				user["usage"] += download["size"]
				bisect.insort(users, user)

		for job in jobs: job.join()