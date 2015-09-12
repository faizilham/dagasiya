from models import Model, enum, timestamp
from datetime import datetime
from tinydb import where

"""
	SCHEMA
	{
		"name": the user name
		"passwd": user password
		"quota": MB of maximum usage
		"usage": MB of usage for the day
		"timestamp": last update timestamp
	}
"""

class ProxyUsers(Model):
	def __init__(self, dbpath):
		Model.__init__(self, dbpath, "proxy_users")

	def set_user(self, name, passwd, quota):
		user = self.db.get(where("name") == name)
		current = timestamp()
		if user:
			user["passwd"] = passwd; user["quota"] = quota

			midnight = datetime(current.year, current.month, current.day, 0, 0, 0)

			if user["timestamp"] < midnight:
				user["timestamp"] = current
				user["usage"] = 0

			self.db.update(user, where("name") == name)
		else:
			self.db.insert({"name": name, "passwd": passwd, "quota": quota, "usage": 0, "timestamp": current})

	def get_user(self, name):
		return db.get(where("name") == name)

	def add_usage(self, name, usage):
		def inc_usage(element):
			element["usage"] += usage
			element["timestamp"] = timestamp()

		self.db.update(inc_usage, where("name") == name)

	def refresh_quotas(self):
		current = timestamp()
		midnight = datetime(current.year, current.month, current.day, 0, 0, 0)

		self.db.update({"usage": 0, "timestamp": current}, where("timestamp") < midnight)

	def delete(self, name):
		self.db.remove(where("name") == name)