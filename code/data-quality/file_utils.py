from progress_bar import ProgressBar

class FileUtils:
	def __init__(self, folder, filename):
		self.full_filename = folder + "/" + filename
		self.filename = filename
		self.total_lines = self.file_length()
		self.progress_bar = ProgressBar(self.total_lines)

	def print_file_data(self):
		print "Parsing " + self.filename
		print "Total lines: " + str(self.total_lines)

	def print_progress(self, current_line):
		self.progress_bar.print_progress(current_line)

	def file_length(self):
		with open(self.full_filename) as f:
			for i, l in enumerate(f):
				pass
		return i + 1