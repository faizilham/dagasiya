import config
from models import downloads, proxy_users
from helpers import servers
class Dagasiya:
	def __init__(self):
		self.config = config.config
		self.servers = servers.Servers(self.config.get("servers"))

		self.downloads = downloads.Downloads(self.config["db_folder"])
		self.users = proxy_users.ProxyUsers(self.config["db_folder"])
		self.init_user()

	def init_user(self):
		users = self.config["proxy"]["users"]

		for user in users:
			self.users.set_user(user["name"], user["passwd"], user["quota"])

if __name__ == "__main__":
	dagasiya = Dagasiya()