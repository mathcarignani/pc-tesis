from file_utils import * 

# This class is used to find different rows with the same date.
class RepeatFinder:
	def __init__(self, folder, filename):
		self.file_utils = FileUtils(folder, filename)
		self.current_line = 0
		self.header = True
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

	def parse_line(self, line):
		s_line = line.split()
		if not(self.header):
			current_date = s_line[0]
			if current_date == self.last_date:
				print 'ERROR', current_date
			self.last_date = current_date
		else:
			if s_line[0][0] == '2': # first date
				self.last_date = s_line[0]
				self.header = False
