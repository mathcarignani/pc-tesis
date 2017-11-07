from progress_bar import ProgressBar
import time


class FileReader:
    def __init__(self, folder, filename):
        self.full_filename = folder + "/" + filename
        self.filename = filename
        self.total_lines = self._total_lines()
        self.current_line = 0

    def parse_file(self, parser):
        print "Parsing '" + self.filename + "'"
        start = time.time()
        self._process_file(parser)
        self._print_elapsed(start)

    def _process_file(self, parser):
        progress_bar = ProgressBar(self.total_lines)

        with open(self.full_filename, "r") as open_file:
            for line in open_file:
                parser.parse_line(line)
                self.current_line += 1
                progress_bar.print_progress(self.current_line)
            # if self.current_line == 1000:
            # 	break

    def _total_lines(self):
        return sum(1 for line in open(self.full_filename, 'rb'))

    def _print_elapsed(self, start):
        end = time.time()
        elapsed = end - start
        print "Time elapsed:", elapsed, "seconds"
