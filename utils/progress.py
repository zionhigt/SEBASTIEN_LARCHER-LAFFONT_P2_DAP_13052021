import sys
import time
#from singleton import Singleton

class Progress(object):
	def __init__(self, steps, view_type, msg_start, msg_end):
		'''
		def __init__(self, steps: int, view_type: in ['percent', 'fraction', 'unique'], message: str)
		'''
		#self.__new__()
		self.steps = steps
		self.view_type = view_type
		self.msg_start = msg_start
		self.msg_end = msg_end

	def update(self, step=0):
		sys.stdout.flush()
		sys.stdout.write('\r{} : {}/{} {}'.format(self.msg_start, step, self.steps, self.msg_end))
if __name__ == '__main__':
	help(Progress)
# category.csv... X/Y lignes have been written
	 