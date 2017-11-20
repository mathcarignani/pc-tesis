from progress_bar import ProgressBar
import time


class FileWriter:
    def __init__(self, folder, filename):
        self.full_filename = folder + "/" + filename
        self.filename = filename
        self.written_lines = 0

    def write_file(self, cleaner_vwc):
        print "Writing '" + self.filename + "'"
        start = time.time()
        self._process_file(cleaner_vwc)
        self._print_elapsed(start)

    def _process_file(self, cleaner_vwc):
        progress_bar = ProgressBar(cleaner_vwc.total_lines)
        with open(self.full_filename, 'w') as open_file:
            while not cleaner_vwc.has_finished():
                line = cleaner_vwc.generate_line()
                open_file.write(line + '\n')
                self.written_lines += 1
                progress_bar.print_progress(self.written_lines)

    def _print_elapsed(self, start):
        end = time.time()
        elapsed = end - start
        print "Time elapsed:", elapsed, "seconds"
