class Singleton(object):
	__instance = None
	def __new__(cls):
		if not cls.__instance:
			cls.__instance = cls
		return cls