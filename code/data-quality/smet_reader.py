import pandas as pd
import numpy as np
from progress import print_progress


class Data:
	def __init__(self):
		self.df = None

	def parse_header(self, s_line):
		if s_line[0] == 'fields':
			# EXAMPLE:
			# fields       = timestamp TA TSS TSG VW DW VW_MAX ISWR OSWR ILWR PSUM HS RH
			self.df = pd.DataFrame(columns=s_line[3:])
		return s_line[0] != '[DATA]'

	def parse_data(self, s_line):
		# EXAMPLE:
		# 2009-10-01T01:00  278.92   273.89   273.89    1.4     0    0.0      0      0 263.637  0.000    0.000   0.926
		timestamp = pd.to_datetime(s_line[0])
		self.df.loc[timestamp] = np.array(s_line[1:]).astype(np.float)


class FileUtils:
	def __init__(self, folder, filename):
		self.full_filename = folder + "/" + filename
		self.filename = filename
		self.total_lines = self.file_length()

	def print_file_data(self):
		print "Parsing " + self.filename
		print "Total lines: " + str(self.total_lines)

	def progress(self, current_line):
		print_progress(current_line, self.total_lines)

	def file_length(self):
		with open(self.full_filename) as f:
			for i, l in enumerate(f):
				pass
		return i + 1


class SMETReader:
	def __init__(self, folder, filename):
		self.file_utils = FileUtils(folder, filename)
		self.data = Data()
		self.current_line = 0
		self.header = True

	def parse_file(self):
		self.file_utils.print_file_data()
		with open(self.file_utils.full_filename, "r") as smet_file:
			for line in smet_file:
				self.parse_line(line)
				self.current_line += 1
				if self.current_line == 1000:
					break
		return self.data.df

	def parse_line(self, line):
		s_line = line.split()
		if self.header:
			self.header = self.data.parse_header(s_line)
		else:
			self.data.parse_data(s_line)
			self.file_utils.progress(self.current_line)
