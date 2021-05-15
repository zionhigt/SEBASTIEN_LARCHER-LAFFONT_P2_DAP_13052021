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
		self.decorator_id = 0
		self.decorator_vector = 1

	def update(self, step=0, time_exec=0.001):
		if self.decorator_id == 2:
			self.decorator_vector = -1
			decorator = "..*"
		elif self.decorator_id == 0:
			self.decorator_vector = 1
			decorator = "*.."
		else:
			decorator = '.*.'

		self.decorator_id += self.decorator_vector
		
		sys.stdout.flush()
		# sys.stdout.write('\x1b[2K\r')
		sys.stdout.write('\x1b[2K\r{} : {}/{} {} {} in {}'.format(self.msg_start, step, self.steps, decorator, self.msg_end, time_exec))
if __name__ == '__main__':
	help(Progress)
# category.csv... X/Y lignes have been written
	 