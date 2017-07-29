# from data import *
# from smet_reader import *
# from vwc_reader import *
# import time

filename = "/home/pablo/Documents/tesis/pc-tesis/code/data-quality/output2/vwc.txt"
with open(filename, "r") as data_file:
	null_mode = False
	total = 0
	total_columns = 10
	for line in data_file:
		s_line = line.split()
		if len(s_line) > 0:
			if not(null_mode):
				# Parsing vwc_222.smet
				if s_line[0] == "Parsing":
					print "FILE:", s_line[1]
				# Time elapsed: 60.4806778431 sec	
				elif s_line[0] == "Time" and s_line[1] == "elapsed:":
					# print line
					pass
				# Total dataset length: 26304
				elif s_line[0] == "Total" and s_line[1] == "dataset":
					total = int(s_line[3])
					print "Total length", total
				# Null values count:
				elif s_line[0] == "Null" and s_line[1] == "values":
					null_mode = True
			# dtype: int64
			elif s_line[0] == "dtype:" and s_line[1] == "int64":
				null_mode = False
				total = 0
				print "total_columns:", total_columns
				total_columns = 10
				print
			# -10cm_A      3969
			else:
				count = int(s_line[1])
				if count == total:
					total_columns -= 1
				percentage = 100 * float(count)/float(total)
				# print count, "=>", "{0:.2f}".format(percentage), "%"


