import sys
import time
#from singleton import Singleton

class Progress(object):
	def __init__(self, steps, view_type, message):
		'''
		def __init__(self, steps: int, view_type: in ['percent', 'fraction', 'unique'], message: str)
		'''
		#self.__new__()
		self.steps = steps
		self.view_type = view_type
		self.message = message

	def update(self, step=0):
		sys.stdout.flush()
		sys.stdout.write('\r{} : {}/{}'.format(self.message, step, self.steps))
if __name__ == '__main__':
	help(Progress)

	 