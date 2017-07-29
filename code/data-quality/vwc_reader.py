from data import * 
from file_utils import * 

class VWCReader:
	def __init__(self, folder, filename):
		self.file_utils = FileUtils(folder, filename)
		self.data = Data()
		self.current_line = 0
		self.last_date = None

	def parse_file(self):
		self.file_utils.print_file_data()
		with open(self.file_utils.full_filename, "r") as smet_file:
			for line in smet_file:
				self.parse_line(line)
				self.file_utils.print_progress(self.current_line)
				self.current_line += 1
				# if self.current_line == 1000:
				# 	break
		print
		return self.data

	def parse_line(self, line):
		s_line = line.split()
		if self.current_line != 0:
			self.data.parse_data(s_line, line)
		else: # first line
			self.data.parse_fields(s_line)
			self.data.set_nodata()
