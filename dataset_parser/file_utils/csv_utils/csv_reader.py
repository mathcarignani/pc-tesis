import csv
from aux.progress_bar import ProgressBar
from file_utils.aux import full_path


class CSVReader:
    def __init__(self, path, filename, progress=False):
        path = full_path(path, filename)
        self.continue_reading = True
        self.file = open(path, "r")
        self.csv_reader = csv.reader(self.file)
        if progress:
            total_lines = self._total_lines(path)
            self.progress_bar = ProgressBar(total_lines)
        else:
            self.progress_bar = None
        self.current_row_count = 0
        self.previous_row = next(self.csv_reader, None)

    # PRE: self.continue_reading
    def read_row(self):
        previous_row = self.previous_row
        row = next(self.csv_reader, None)
        if not row:
            self.continue_reading = False
        else:
            self.current_row_count += 1
            self.print_progress()
            self.previous_row = row

        return previous_row

    def _total_lines(self, path):
        return sum(1 for _ in csv.reader(open(path, "r")))

    def close(self):
        self.file.close()

    def print_progress(self):
        if self.progress_bar:
            self.progress_bar.print_progress(self.current_line_count)
