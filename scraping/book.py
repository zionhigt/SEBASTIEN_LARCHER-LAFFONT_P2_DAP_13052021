#get a book
class Book(object):
	def __init__(self, msg):
		self.msg = msg
	def say(self):
		print(self.msg if self.msg else '')