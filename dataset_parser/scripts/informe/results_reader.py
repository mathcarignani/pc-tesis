import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from scripts.informe.results_constants import ResultsConstants


class ResultsReader(object):
    def __init__(self, file_key, file_value):
        if file_value in [0, 3]:
            input_path, input_filename = ResultsConstants.get_path_and_filename(file_key, file_value)
        else:
            input_path, input_filename = file_key, file_value
        self.input_file = CSVReader(input_path, input_filename)

    def read_line_no_count(self):
        return self.input_file.read_line()

    def read_line(self):
        self.line_count += 1
        self.line = self.input_file.read_line()
        return self.line

    @staticmethod
    def matching_line(line, index, value, is_integer):
        value_in_index = line[index]
        if len(value_in_index) == 0:
            return False
        value_to_compare = int(value_in_index) if is_integer else value_in_index
        return value == value_to_compare

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0

    def find_dataset(self, dataset_name):
        self.__goto_file_start()
        self.__find_next_line(0, dataset_name, False)

    def find_filename(self, filename):
        self.__goto_file_start()
        self.__find_next_line(1, filename, False)

    def continue_reading(self):
        return self.input_file.continue_reading

    def __find_next_line(self, index, value, is_integer):
        if self.line_count > 0 and ResultsReader.matching_line(self.line, index, value, is_integer):
            return True

        while self.input_file.continue_reading:
            self.read_line()
            if ResultsReader.matching_line(self.line, index, value, is_integer):
                return True
        raise Exception("ERROR: __find_next_line")