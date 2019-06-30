import sys
sys.path.append('.')

from scripts.compress.compress_aux import DATASETS_ARRAY, dataset_csv_filenames
from scripts.avances14.script_0vs3 import matching_line
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter


class GlobalizeResults(object):
    #
    # Converts the results in "complete-mask-mode=3.csv" file so that the results of multiple files are merged
    #
    def __init__(self, input_path, input_file, output_path, output_file):
        self.input_file = CSVReader(input_path, input_file)
        self.output_file = CSVWriter(output_path, output_file)
        for dataset_obj in DATASETS_ARRAY:
            self.__globalize_dataset(dataset_obj['name'])

    def __globalize_dataset(self, dataset_name):
        filenames = dataset_csv_filenames(dataset_name)
        if len(filenames) == 1:
            self.__copy_dataset(dataset_name)
        else:
            self.__merge_results(dataset_name, filenames)

    #
    # single file, copy everything until another dataset starts
    #
    def __copy_dataset(self, dataset_name):
        self.__find_dataset(dataset_name)
        self.__copy_until_change(0)

    #
    # multiple files, globalize results
    #
    def __merge_results(self, dataset_name, filenames):
        results_array = self.__results_array(dataset_name, filenames)
        # TODO: sum results

    def __results_array(self, dataset_name, filenames):
        print dataset_name
        self.__find_dataset(dataset_name)
        results = []
        for filename in filenames:
            self.__find_filename(filename)
            filename_results = self.__add_until_change(1)
            assert(len(filename_results) == 457)  # total number of rows for a file
            results.append(filename_results)
        assert(len(results) == len(filenames))
        return results

    def __copy_until_change(self, line_index):
        first_line = True
        while self.input_file.continue_reading and (first_line or len(self.line[line_index]) == 0):
            self.output_file.write_row(self.line)
            self.__read_line()
            first_line = False

    def __add_until_change(self, line_index):
        lines_array = []
        first_line = True
        while self.input_file.continue_reading and (first_line or len(self.line[line_index]) == 0):
            lines_array.append(self.line)
            self.__read_line()
            first_line = False
        return lines_array

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0

    def __read_line(self):
        self.line = self.input_file.read_line()
        self.line_count += 1

    def __find_dataset(self, dataset_name):
        self.__goto_file_start()
        self.__find_next_line(0, dataset_name, False)

    def __find_filename(self, filename):
        self.__goto_file_start()
        self.__find_next_line(1, filename, False)

    def __find_next_line(self, index, value, is_integer):
        if self.line_count > 0 and matching_line(self.line, index, value, is_integer):
            return True

        while self.input_file.continue_reading:
            self.__read_line()
            if matching_line(self.line, index, value, is_integer):
                return True
        raise Exception("ERROR: __find_next_line")


input_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/2-complete"
input_file = "complete-mask-mode=3.csv"
output_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-18"
output_file = "complete-mask-mode=3-global.csv"

GlobalizeResults(input_path, input_file, output_path, output_file)
