import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.math_utils import MathUtils

path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances/avances-13/"
path_complete = path + "2-complete/"
path_0vs3 = path + "3-0vs3/"


class RemoveFrom3(object):
    def __init__(self):
        self.input_file = CSVReader(path_complete, "complete-mask-mode=3.csv")
        self.output_file = CSVWriter(path_0vs3, "complete-mask-mode=3-remove.csv")

    def run(self):
        current_coder = None
        while self.input_file.continue_reading:
            line = self.input_file.read_line()
            current_coder = line[3] if len(line[3]) > 0 else current_coder
            if current_coder not in ['CoderFR', 'CoderSF']:
                self.output_file.write_row(line)
        self.close_files()

    def close_files(self):
        self.input_file.close()
        self.output_file.close()

# RemoveFrom3().run()


class Params(object):
    def __init__(self):
        self.filename = None
        self.coder = None
        self.threshold = None
        self.window = None
        self.total = 1
        self.results = {}
        self.mode = "Filenames" # "Coders"
        self.rel_diff = None

    def update(self, line):
        # Dataset	Filename	#rows	Coder	%	Error Threshold	Window Param
        self.filename = self.set_param(line[1], self.filename)
        self.coder = self.set_param(line[3], self.coder)
        self.threshold = self.set_param(line[4], self.threshold)
        self.window = self.set_param(line[6], self.window)

    def print_params(self, index, rel_diff):
        print(str(self.total) + ") " + self.filename + " - " + self.coder +
              " - THRE=" + self.threshold + " - W=" + self.window + " - IN=" + str(index))
        self.check_relative_diff(rel_diff)
        self.update_results()
        self.total += 1

    def check_relative_diff(self, rel_diff):
        if "noaa_spc" not in self.filename:
            return

        self.rel_diff = rel_diff if (self.rel_diff is None or self.rel_diff < rel_diff) else self.rel_diff

    def update_results(self):
        if self.filename in self.results:
            if self.mode == "Filenames":
                self.results[self.filename] += 1
            elif self.mode == "Coders":
                if self.coder in self.results[self.filename]:
                    self.results[self.filename][self.coder] += 1
                else:
                    self.results[self.filename][self.coder] = 1
        else:
            if self.mode == "Filenames":
                self.results[self.filename] = 1
            elif self.mode == "Coders":
                self.results[self.filename] = {}
                self.results[self.filename][self.coder] = 1

    def print_results(self):
        for filename in sorted (self.results.keys()):
            if self.mode == "Filenames":
                print filename + " -> " + str(self.results[filename])
            elif self.mode == "Coders":
                for coder in self.results[filename]:
                    print filename + " - " + coder + " -> " + str(self.results[filename][coder])
        print "Max Rel diff = " + str(self.rel_diff)

    def set_param(self, new_value, old_value):
        return new_value if len(new_value) > 0 else old_value


class Compare0vs3(object):
    SIZE_TOTAL_FIRST_INDEX = 15  # "Other columns - Size (total)"

    def __init__(self):
        self.reader0 = CSVReader(path_complete, "complete-mask-mode=0.csv")
        self.reader3 = CSVReader(path_0vs3, "complete-mask-mode=3-remove.csv")
        assert(self.reader0.total_lines == self.reader3.total_lines)
        self.writer = CSVWriter(path_0vs3, "0vs3.csv")
        self.params = Params()

    def run(self):
        line_count = 0
        while self.reader0.continue_reading:
            line0, line3 = self.reader0.read_line(), self.reader3.read_line()
            self.params.update(line0)
            new_line = self.process_line(line0, line3, line_count)
            self.writer.write_row(new_line)
            line_count += 1
        self.close_files()

    def process_line(self, line0, line3, line_count):
        new_line = self.compare_lines(line0, line3)
        if line_count == 0:
            assert(line0[self.SIZE_TOTAL_FIRST_INDEX] == "Other columns - Size (total)")
            new_line += ['Other columns - Size (total) - MASK_MODE=0'] + [None] * 6
            new_line += ['Other columns - Size (total) - MASK_MODE=3'] + [None] * 6
        else:
            new_line += self.results(line0, line3)
        return new_line

    def compare_lines(self, line0, line3):
        # Dataset	Filename	#rows	Coder	%	Error Threshold	Window Param
        assert(len(line0) == len(line3))
        assert(line0[:7] == line3[:7])
        return line0[:7]

    def results(self, line0, line3):
        col_index, line_index = 1, self.SIZE_TOTAL_FIRST_INDEX
        results0, results3 = [], []
        while line_index < len(line0):
            res0, res3 = int(line0[line_index]), int(line3[line_index])
            if res0 == res3:
                self.append_same_results(results0, results3, res0)
            elif res0 < res3:
                rel_diff = self.append_results(results0, results3, res0, res3)
                self.params.print_params(col_index, rel_diff)
            else:  # res3 < res0
                self.append_results(results3, results0, res3, res0)
            col_index += 1
            line_index += 4
        return self.complete_line(results0) + self.complete_line(results3)

    def append_results(self, best_list, worst_list, best, worst):
        rel_diff = MathUtils.relative_diff(worst, best)
        best_list.append(MathUtils.int_to_str(best) + " - B")
        worst_list.append(MathUtils.int_to_str(worst) + " - W - " + str(rel_diff))
        return rel_diff

    def append_same_results(self, results0, results3, res):
        results0.append(MathUtils.int_to_str(res) + " - S")
        results3.append(MathUtils.int_to_str(res) + " - S")

    # complete so that results have length = 7
    def complete_line(self, results):
        return results + [None] * (7 - len(results))

    def close_files(self):
        self.reader0.close()
        self.reader3.close()
        self.writer.close()
        self.params.print_results()

Compare0vs3().run()
