from tinydb import TinyDB
from datetime import datetime

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

def timestamp():
	return datetime.now().strftime(TIMEFORMAT)

def parse_timestamp(tstamp):
	return datetime.strptime(tstamp, TIMEFORMAT)

def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)

class Model:
	def __init__(self, dbpath, dbname):
		self.db = TinyDB("{0}/{1}.json".format(dbpath, dbname))

	def all(self):
		return self.db.all()