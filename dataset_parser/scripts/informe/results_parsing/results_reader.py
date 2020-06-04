import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.results_parsing.results_paths import ResultsPaths
from scripts.informe.math_utils import MathUtils

#
# This class is used for parsing the results of the results.csv file, which is created when running compress_script.py
#
class ResultsReader(object):
    def __init__(self, file_key, file_mode):
        if file_mode in [0, 3]:
            input_path, input_filename = ResultsPaths.get_path_and_filename(file_key, file_mode)
        else:
            input_path, input_filename = file_key, file_mode
        self.input_file = CSVReader(input_path, input_filename)

    def read_line_no_count(self):
        return self.input_file.read_line()

    def __read_line(self):
        self.line_count += 1
        self.line = self.input_file.read_line()
        return self.line

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0

    def full_results(self):
        self.__goto_file_start()
        self.__read_line()  # headers line
        lines_array = []
        while self.continue_reading():
            self.__read_line()
            lines_array.append(self.line)
        return lines_array

    def dataset_results(self, dataset_name, change_index=CSVConstants.INDEX_DATASET):
        self.find_dataset(dataset_name)
        return ResultsReader.add_until_change(self, change_index)

    def filename_results(self, dataset_name, filename, change_index=CSVConstants.INDEX_FILENAME):
        self.find_filename_in_dataset(dataset_name, filename)
        return ResultsReader.add_until_change(self, change_index)

    def find_dataset(self, dataset_name):
        self.__goto_file_start()
        self.__find_next_line(CSVConstants.INDEX_DATASET, dataset_name, False)

    def find_filename(self, filename):
        self.__goto_file_start()
        self.__find_next_line(CSVConstants.INDEX_FILENAME, filename, False)

    def find_threshold(self, threshold):
        # self.__goto_file_start()
        self.__find_next_line(CSVConstants.INDEX_THRESHOLD, threshold, True)

    def find_filename_in_dataset(self, dataset_name, filename):
        self.find_dataset(dataset_name)
        self.__find_next_line(CSVConstants.INDEX_FILENAME, filename, False)

    def continue_reading(self):
        return self.input_file.continue_reading

    def __find_next_line(self, index, value, is_integer):
        if self.line_count > 0 and ResultsReader.matching_line(self.line, index, value, is_integer):
            return True

        while self.input_file.continue_reading:
            self.__read_line()
            if ResultsReader.matching_line(self.line, index, value, is_integer):
                return True
        raise Exception("ERROR: __find_next_line")

    @staticmethod
    def matching_line(line, index, value, is_integer):
        value_in_index = line[index]
        if len(value_in_index) == 0:
            return False
        value_to_compare = int(value_in_index) if is_integer else value_in_index
        return value == value_to_compare

    @staticmethod
    def copy_until_change(results_reader, output_file, line_index):
        first_line = True
        while results_reader.continue_reading() and (first_line or len(results_reader.line[line_index]) == 0):
            output_file.write_row(results_reader.line)
            results_reader.__read_line()
            first_line = False
        if not results_reader.continue_reading():
            output_file.write_row(results_reader.line)

    @staticmethod
    def add_until_change(results_reader, line_index):
        lines_array = []
        first_line = True
        while results_reader.continue_reading() and (first_line or len(results_reader.line[line_index]) == 0):
            lines_array.append(results_reader.line)
            results_reader.__read_line()
            first_line = False
        if not results_reader.continue_reading():
            lines_array.append(results_reader.line)
        return lines_array

    @staticmethod
    def set_percentages(line, line_total):
        assert(len(line) == len(line_total))
        for index in range(len(line)):
            if CSVConstants.is_percentage_index(index):
                total, value = line_total[index-1], line[index-1]
                percentage = MathUtils.calculate_percent(total, value)
                line[index] = percentage
        return line

    @staticmethod
    def convert_lines(lines):
        return [ResultsReader.convert_line(line) for line in lines]

    @staticmethod
    def convert_line(line):
        new_line = []
        #    0         1        2     3    4         5                6
        # Dataset, Filename, #rows, Coder, %, Error Threshold, Window Param
        #
        new_line.append(line[CSVConstants.INDEX_DATASET])
        new_line.append(line[CSVConstants.INDEX_FILENAME])

        no_rows = line[CSVConstants.INDEX_NO_ROWS]
        new_line.append(MathUtils.str_to_int(no_rows) if isinstance(no_rows, int) else '')

        new_line.append(line[CSVConstants.INDEX_ALGORITHM])  # Coder
        threshold = line[CSVConstants.INDEX_THRESHOLD]
        new_line.append(int(threshold) if len(threshold) > 0 else None)  # %
        new_line.append('')  # Error Threshold
        window = line[CSVConstants.INDEX_WINDOW]
        new_line.append(int(window) if len(window) > 0 else None)  # Window Param

        #    7         8             9                     10                  11                 12
        # Size (B), CR (%), Delta - Size (data), Delta - Size (mask), Delta - Size (total), Delta - CR (%), ...
        #
        for index in range(CSVConstants.INDEX_TOTAL_SIZE, len(line)):
            if CSVConstants.is_percentage_index(index):
                value = line[index]
                if value.count('.') > 1:  # e.g. "1.145.49"
                    value = value.replace('.', '', 1)  # "1.145.49" => "1145.49"
                new_line.append(float(value))
            else:
                new_line.append(MathUtils.str_to_int(line[index]))
        return new_line