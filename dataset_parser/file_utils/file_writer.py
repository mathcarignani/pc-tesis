from progress_bar import ProgressBar
import time


class FileWriter:
    def __init__(self, folder, filename):
        self.filename = filename
        self.written_lines = 0
        self.file = open(folder + "/" + filename, "w")

    def write_line(self, line):
        self.file.write(line + '\n')
        self.written_lines += 1

    def close(self):
        self.file.close()

    # def write_file(self, cleaner_vwc):
    #     print "Writing '" + self.filename + "'"
    #     start = time.time()
    #     self._process_file(cleaner_vwc)
    #     self._print_elapsed(start)
    #
    # def _process_file(self, cleaner_vwc):
    #     progress_bar = ProgressBar(cleaner_vwc.total_lines)
    #
    #     while not cleaner_vwc.has_finished():
    #         line = cleaner_vwc.generate_line()
    #         self.write_line(line)
    #         progress_bar.print_progress(self.written_lines)
    #     self.file.close()
    #
    # def _print_elapsed(self, start):
    #     end = time.time()
    #     elapsed = end - start
    #     print "Time elapsed:", elapsed, "seconds"
