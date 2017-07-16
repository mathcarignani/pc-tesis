from progress import print_progress

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