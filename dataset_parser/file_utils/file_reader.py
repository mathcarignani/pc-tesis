from aux.progress_bar import ProgressBar
from utils import Utils
# import time


class FileReader:
    def __init__(self, path, filename, progress=False):
        self.full_path = Utils.full_path(path, filename)
        self.total_lines = self._total_lines()
        self.continue_reading = True
        self.file = open(self.full_path, "r")
        self.progress_bar = ProgressBar(self.total_lines) if progress else None
        self.current_line_count = 0
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

    def _total_lines(self):
        return sum(1 for line in open(self.full_path, 'rb'))

    def close(self):
        self.file.close()

    def print_progress(self):
        if self.progress_bar:
            self.progress_bar.print_progress(self.current_line_count)

    # def parse_file(self, parser):
    #     print "Parsing '" + self.filename + "'"
    #     start = time.time()
    #     self._process_file(parser)
    #     self._print_elapsed(start)

    # def _process_file(self, parser):
    #     progress_bar = ProgressBar(self.total_lines)
    #
    #     while True:
    #         line = self.file.readline()
    #         if not line:
    #             break
    #         else:
    #             parser.parse_line(line)
    #             self.current_line += 1
    #             progress_bar.print_progress(self.current_line)
    #             # if self.current_line == 1000:
    #             # 	break
    #     self.close()

    # def _print_elapsed(self, start):
    #     end = time.time()
    #     elapsed = end - start
    #     print "Time elapsed:", elapsed, "seconds"


