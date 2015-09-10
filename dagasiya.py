import json
import config

class Dagasiya:
	def __init__(self):
		self.config = config.config

	def reload_conf(self):
		reload(config)
		self.initconf()


if __init__ == "__main__":
	pass