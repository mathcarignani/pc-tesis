import csv
from aux.progress_bar import ProgressBar
from file_utils.aux import full_path


class CSVReader:
    def __init__(self, path, filename, progress=False):
        self.path, self.filename = path, filename
        self.full_path = full_path(path, filename)
        self.continue_reading = True
        self.file = open(self.full_path, "r")
        self.csv_reader = csv.reader(self.file)
        self.total_lines = self.total_lines_()
        self.current_line_count = 0
        self.progress_bar = None if not progress else self.new_progress_bar()
        self.previous_row = next(self.csv_reader, None)

    # PRE: self.continue_reading
    def read_line(self):
        previous_row = self.previous_row
        row = next(self.csv_reader, None)
        if not row:
            self.continue_reading = False
        else:
            self.current_line_count += 1
            self.print_progress()
            self.previous_row = row

        return previous_row

    def total_lines_(self):
        return sum(1 for _ in csv.reader(open(self.full_path, "r")))

    def close(self):
        self.file.close()

    def new_progress_bar(self):
        self.progress_bar = ProgressBar(self.total_lines - self.current_line_count)

    def print_progress(self):
        if self.progress_bar:
            self.progress_bar.print_progress()
