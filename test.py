import sys
import csv
import time

for i in range(10):
	star_load = '*'*i
	dot_load = '.'*(10-i)
	load = "\r[{}{}] => {}/10".format(star_load, dot_load, i)
	sys.stdout.write("")
	sys.stdout.flush()
	sys.stdout.write(load)
	time.sleep(1)
