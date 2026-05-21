from clickhouse_connect import get_client
from json import loads
from random import random

class CH:
	def __init__(self):
		self._client = None

	def connect(self):
		# self._client = get_client(host='localhost', username='admin', password='!5tronG')
		self._client = get_client(host='clickhouse', username='admin', password='!5tronG')


	def close(self):
		self._client.close()

	def query(self, data: dict):
		# data = { 
		# 	"action": "insert",
		# 	"table": "test",
		# 	"columns": ['key', 'value', 'metric'],
		# 	"data": [
		# 		[1000, 'String Value 1000', 5.233],
		# 		(2000, 'String Value 2000', -107.04),
		# 	]
		# }
		#print(data)
		func = getattr(self, "q___" + data.get("action"), None)
		return func(data) if func else { "error": "unknown command" }
	

	def q___select(self, data: dict):
		return self._client.query(data.get("query")).result_rows

