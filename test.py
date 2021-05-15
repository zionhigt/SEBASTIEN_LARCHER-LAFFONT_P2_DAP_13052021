import sys
import csv
import time

# for i in range(10):
# 	star_load = '*'*i
# 	dot_load = '.'*(10-i)
# 	load = "\r[{}{}] => {}/10".format(star_load, dot_load, i)
# 	sys.stdout.write("")
# 	sys.stdout.flush()
# 	sys.stdout.write(load)
# 	time.sleep(1)


sys.stdout.write("11111\r")
sys.stdout.flush()
time.sleep(1)
sys.stdout.write("2222222222\r")
sys.stdout.flush()
time.sleep(1)
sys.stdout.write('\x1b[2K\r')
sys.stdout.flush()
# time.sleep(1)
sys.stdout.write("11111\r")
sys.stdout.flush()


