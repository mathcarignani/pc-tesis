from auxi.progress_bar import ProgressBar
from file_utils.auxi import full_path


class TextFileReader:
    def __init__(self, path, filename, progress=False):
        self.path, self.filename = path, filename
        f_path = full_path(path, filename)
        self.continue_reading = True
        self.file = open(f_path, "r")
        self.total_lines = self._total_lines(f_path)
        self.current_line_count = 0
        self.progress_bar = None if not progress else self.new_progress_bar()
        self.previous_line = self.file.readline()

    # PRE: self.continue_reading
    def read_line(self):
        previous_line = self.previous_line
        line = self.file.readline()
        if not line:
            self.continue_reading = False
        else:
            self.current_line_count += 1
            self.print_progress()
            self.previous_line = line
        return previous_line

    def _total_lines(self, path):
        return sum(1 for _ in open(path, 'rb'))

    def close(self):
        self.file.close()

    def new_progress_bar(self):
        self.progress_bar = ProgressBar(self.total_lines - self.current_line_count)

    def print_progress(self):
        if self.progress_bar:
            self.progress_bar.print_progress()
