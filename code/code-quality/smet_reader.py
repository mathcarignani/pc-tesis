import pandas as pd
from progress import print_progress

class SMETReader:
	def __init__(self, folder, filename):
		self.full_filename = folder + "/" + filename
		self.filename = filename
		self.total_lines = self.file_length();
		self.last_line = 0
		self.df = pd.DataFrame({})

	def parse(self):
		print "Parsing " + self.filename
		print "Total lines: " + str(self.total_lines)
		with open(self.full_filename, "r") as smet_file:
			for line in smet_file:
				self.parse_line()
				self.last_line += 1
				print_progress(self.last_line, self.total_lines)
		print self.last_line


	def parse_line(self):
		pass

	def file_length(self):
		with open(self.full_filename) as f:
			for i, l in enumerate(f):
				pass
		return i + 1




folder = "/media/pablo/78FA-ED53/data-quality/datasets/1-davos/IRKISsoilmoisturedata/interpolatedmeteo"
filename = "interpolatedmeteo_222.smet"
smet_reader = SMETReader(folder, filename)
smet_reader.parse()
