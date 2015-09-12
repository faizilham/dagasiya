from datetime import datetime
from tinydb import TinyDB, where
from tinydb.middlewares import SerializationMiddleware
from tinydb.serialize import Serializer
from tinydb.storages import JSONStorage

class DateTimeSerializer(Serializer):
	OBJ_CLASS = datetime
	FORMAT = "%Y-%m-%dT%H:%M:%S"

	def encode(self, obj):
		return obj.strftime(self.FORMAT)

	def decode(self, s):
		return datetime.strptime(s, self.FORMAT)

def timestamp():
	return datetime.now()

def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	return type('Enum', (), enums)

class Model:
	def __init__(self, dbpath, dbname):
		path = "{0}/{1}.json".format(dbpath, dbname)

		serializer = SerializationMiddleware(JSONStorage)
		serializer.register_serializer(DateTimeSerializer(), 'TinyDate')
		self.db = TinyDB(path, storage=serializer)

	def all(self):
		return self.db.all()