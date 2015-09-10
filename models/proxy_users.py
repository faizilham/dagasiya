from models import Model, enum, timestamp, parse_timestamp
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
		user = self.db.get(where("name") == name))
		if (user)
			user.passwd = passwd; user.quota = quota

			current = datetime.now()
			midnight = datetime(current.year, current.month, current.day, 0, 0, 0)

			if parse_timestamp(user.timestamp) < midnight:
				user.timestamp = timestamp() 
				user.usage = 0

			self.db.update(user, where("name") == "name")
		else
			self.db.insert({"name": name, "passwd": passwd, "quota": quota, "usage": 0, "timestamp": timestamp()})

	def get_user(self, name):
		return db.get(where("name") == name))

	def update_usage(self, name, usage):
		self.db.update({"usage": usage, "timestamp": timestamp()}, where("name") == name))

	def delete(self, name):
		self.db.remove(where("name") == name))