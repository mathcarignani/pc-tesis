import sys
sys.path.append('.')

from scripts.compress.compress_aux import DATASETS_ARRAY, dataset_csv_filenames
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.avances14.constants import Constants
from scripts.avances11.utils import calculate_percentage
from scripts.informe.results_constants import ResultsConstants
from scripts.informe.results_reader import ResultsReader


class GlobalizeResults(object):
    NUMBER_OF_ROWS = {0: 393, 3: 457}

    #
    # Converts the results in "complete-mask-mode=3.csv" file so that the results of multiple files are merged
    #
    def __init__(self, value, output_path, output_file):
        self.value = value
        self.number_of_rows = GlobalizeResults.NUMBER_OF_ROWS[value]

        self.input_file_3 = ResultsReader('raw', value)
        self.input_file_0 = ResultsReader('raw', 0)

        self.output_file = CSVWriter(output_path, output_file)
        self.output_file.write_row(self.input_file_3.read_line_no_count())

        for dataset_obj in DATASETS_ARRAY:
            self.__globalize_dataset(dataset_obj['name'])

    def __globalize_dataset(self, dataset_name):
        filenames = dataset_csv_filenames(dataset_name)
        if len(filenames) == 1:
            print dataset_name + " - copy"
            self.__copy_dataset(dataset_name)
        else:
            print dataset_name + " - merge"
            self.__merge_results(dataset_name, filenames)

    #
    # single file, copy everything until another dataset starts
    #
    def __copy_dataset(self, dataset_name):
        self.input_file.find_dataset(dataset_name)
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
        assert(len(results_array[0]) == self.number_of_rows)
        mask_results_lines = self.__mask_results_lines(results_array)

        line0_with_percentages = self.__set_percentages(line0, line0)
        self.output_file.write_row(line0_with_percentages)
        for index, line in enumerate(mask_results_lines):
            if index > 0:  # Ignore MM=3 => CoderBasic
                line_with_percentages = self.__set_percentages(line, line0)
                self.output_file.write_row(line_with_percentages)

    @staticmethod
    def __set_percentages(line, line0):
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
        self.input_file.find_dataset(dataset_name)
        results = []
        for filename in filenames:
            self.input_file.find_filename(filename)
            filename_results = self.__add_until_change(change_index)
            results.append(filename_results)
        assert(len(results) == len(filenames))
        return results

    def __copy_until_change(self, line_index):
        first_line = True
        while self.input_file.continue_reading() and (first_line or len(self.input_file.line[line_index]) == 0):
            self.output_file.write_row(self.input_file.line)
            self.input_file.read_line()
            first_line = False

    def __add_until_change(self, line_index):
        lines_array = []
        first_line = True
        while self.input_file.continue_reading() and (first_line or len(self.input_file.line[line_index]) == 0):
            lines_array.append(self.input_file.line)
            self.input_file.read_line()
            first_line = False
        return lines_array


def run(value):
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-18"
    output_file = "complete-mask-mode=" + str(value) + "-global.csv"
    GlobalizeResults(value, output_path, output_file)

run(0)
run(3)
