import sys
sys.path.append('.')

from scripts.compress.compress_aux import DATASETS_ARRAY, dataset_csv_filenames
from scripts.avances14.script_0vs3 import matching_line
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.avances14.constants import Constants
from scripts.avances11.utils import calculate_percentage
from scripts.informe.results_constants import ResultsConstants


class GlobalizeResults(object):
    NUMBER_OF_LINES = 457
    # NUMBER_OF_LINES = 393

    #
    # Converts the results in "complete-mask-mode=3.csv" file so that the results of multiple files are merged
    #
    def __init__(self, input_path, input_file, input_file_0, output_path, output_file):
        self.input_file_3 = CSVReader(input_path, input_file)
        self.input_file_0 = CSVReader(input_path, input_file_0)
        self.output_file = CSVWriter(output_path, output_file)
        self.output_file.write_row(self.input_file_3.read_line())
        for dataset_obj in DATASETS_ARRAY:
            self.__globalize_dataset(dataset_obj['name'])

    def __globalize_dataset(self, dataset_name):
        print dataset_name
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
        # MM=0 => CoderBasic
        self.input_file = self.input_file_0
        results_array_0 = self.__results_array(dataset_name, filenames, 4)
        assert(len(results_array_0[0]) == 1)
        line0 = self.__mask_results_lines(results_array_0)[0]

        # MM=3 => CoderBasic, CoderPCA, CoderAPCA, etc.
        self.input_file = self.input_file_3
        results_array = self.__results_array(dataset_name, filenames, 1)
        print len(results_array[0])
        assert(len(results_array[0]) == GlobalizeResults.NUMBER_OF_LINES)
        mask_results_lines = self.__mask_results_lines(results_array)

        line0_with_percentages = self.__set_percentages(line0, line0)
        self.output_file.write_row(line0_with_percentages)
        for index, line in enumerate(mask_results_lines):
            if index > 0:  # Ignore MM=3 => CoderBasic
                line_with_percentages = self.__set_percentages(line, line0)
                self.output_file.write_row(line_with_percentages)

    def __set_percentages(self, line, line0):
        assert(len(line) == len(line0))
        for index in range(len(line)):
            if GlobalizeResults.__percentage_index(index):
                total, value = line0[index-1], line[index-1]
                percentage = calculate_percentage(total, value, 2)
                line[index] = percentage
        return line

    def __mask_results_lines(self, results_array):
        new_lines = []
        number_of_rows = len(results_array[0])
        for index in range(number_of_rows):
            new_line = None
            for file_results in results_array:
                file_results_line = file_results[index]
                file_results_line = self.__convert_line(file_results_line)
                new_line = file_results_line if new_line is None else self.__merge_lines(new_line, file_results_line)
            new_lines.append(new_line)
        assert(len(new_lines) == number_of_rows)
        return new_lines

    @staticmethod
    def __percentage_index(index):
        if index < Constants.INDEX_CR_PERCENTAGE:
            return False
        else:
            return (index - Constants.INDEX_CR_PERCENTAGE) % 4 == 0

    @staticmethod
    def __merge_lines(line1, line2):
        assert(line1[Constants.INDEX_ALGORITHM] == line2[Constants.INDEX_ALGORITHM])
        assert(line1[Constants.INDEX_THRESHOLD] == line2[Constants.INDEX_THRESHOLD])
        assert(line1[Constants.INDEX_WINDOW] == line2[Constants.INDEX_WINDOW])
        assert(len(line1) == len(line2))

        for index in range(len(line1)):
            if GlobalizeResults.__percentage_index(index):
                pass
            elif isinstance(line1[index], int):
                line1[index] += line2[index]
        return line1

    @staticmethod
    def __str_to_int(string):
        return int(string.replace(".", ""))

    @staticmethod
    def __convert_line(line):
        print "CONVERT LINE START"
        print line
        new_line = []
        #    0         1        2     3    4         5                6
        # Dataset, Filename, #rows, Coder, %, Error Threshold, Window Param
        #
        new_line.append(line[0])  # Dataset
        new_line.append('Global' if len(line[1]) > 0 else line[1])  # Filename
        new_line.append(GlobalizeResults.__str_to_int(line[2]) if isinstance(line[2], int) else '')  # #rows
        new_line += line[3:5]  # Coder, %
        new_line.append('')  # Error Threshold
        new_line.append(line[6])  # Window Param

        #    7         8             9                     10                  11                 12
        # Size (B), CR (%), Delta - Size (data), Delta - Size (mask), Delta - Size (total), Delta - CR (%), ...
        #
        for index in range(7, len(line)):
            if GlobalizeResults.__percentage_index(index):
                new_line.append("?")
            else:
                new_line.append(GlobalizeResults.__str_to_int(line[index]))
        print "CONVERT LINE END"
        return new_line

    def __results_array(self, dataset_name, filenames, change_index):
        self.__find_dataset(dataset_name)
        results = []
        for filename in filenames:
            self.__find_filename(filename)
            filename_results = self.__add_until_change(change_index)
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


input_file_0 = "complete-mask-mode=0.csv"

input_path, input_filename = ResultsConstants.get_path_and_filename('raw', 3)
# input_path, input_filename = ResultsConstants.get_path_and_filename('raw', 0)

output_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-18"
output_file = "complete-mask-mode=3-global.csv"
# output_file = "complete-mask-mode=0-global.csv"

GlobalizeResults(input_path, input_filename, input_file_0, output_path, output_file)
