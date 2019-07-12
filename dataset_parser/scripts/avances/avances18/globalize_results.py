import sys
sys.path.append('.')

from scripts.compress.compress_aux import DATASETS_ARRAY, dataset_csv_filenames
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.avances.avances18.globalize_utils import GlobalizeUtils
from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.results_reader import ResultsReader


#
# Converts the results in "complete-mask-mode=N.csv" files so that the results of multiple files are merged
#
class GlobalizeResults(object):
    NUMBER_OF_ROWS = {0: 393, 3: 457}

    def __init__(self, value, output_path, output_file):
        self.value = value
        self.number_of_rows = GlobalizeResults.NUMBER_OF_ROWS[value]

        self.input_file_x = ResultsReader('raw', value)

        # The CoderBasic lines have the same values (but not exactly the same format, i.e. "100" vs. "100.0")
        # in these two files, so we can use either one to get the CoderBasic MM=0 values:
        self.input_file_coder_basic = ResultsReader('raw', 0)
        # self.input_file_coder_basic = ResultsReader('basic', 3)

        self.output_file = CSVWriter(output_path, output_file)
        self.output_file.write_row(self.input_file_x.read_line_no_count())

        for dataset_obj in DATASETS_ARRAY:
            self.__globalize_dataset(dataset_obj['name'])

    def __globalize_dataset(self, dataset_name):
        filenames = dataset_csv_filenames(dataset_name)
        if len(filenames) == 1:
            print dataset_name + " - copy"  # there is a single file in the dataset, no need to merge anything
            self.__copy_dataset(dataset_name)
        else:
            print dataset_name + " - merge"
            self.__merge_results(dataset_name, filenames)

    #
    # single file, copy everything until another dataset starts
    #
    def __copy_dataset(self, dataset_name):
        self.input_file.find_dataset(dataset_name)
        ResultsReader.copy_until_change(self.input_file, self.output_file, 0)

    #
    # multiple files, globalize results
    #
    def __merge_results(self, dataset_name, filenames):
        # MM=0 => CoderBasic
        coder_basic_line = self.__get_coder_basic_line(dataset_name, filenames)
        coder_basic_line_with_percentages = ResultsReader.set_percentages(coder_basic_line, coder_basic_line)
        self.output_file.write_row(coder_basic_line_with_percentages)

        # MM=0or3 => CoderBasic, CoderPCA, CoderAPCA, etc.
        other_coders_lines = self.__get_other_coders_lines(dataset_name, filenames)
        GlobalizeUtils.write_other_coders_lines(self.output_file, coder_basic_line, other_coders_lines)

    def __get_coder_basic_line(self, dataset_name, filenames):
        self.input_file = self.input_file_coder_basic
        results_array_0 = self.__results_array(dataset_name, filenames, CSVConstants.INDEX_ALGORITHM)
        assert(len(results_array_0[0]) == 1)
        return self.__mask_results_lines(results_array_0)[0]

    def __get_other_coders_lines(self, dataset_name, filenames):
        self.input_file = self.input_file_x
        results_array = self.__results_array(dataset_name, filenames, CSVConstants.INDEX_FILENAME)
        # print len(results_array[0])
        assert(len(results_array[0]) == self.number_of_rows)
        return self.__mask_results_lines(results_array)

    def __mask_results_lines(self, results_array):
        new_lines = []
        number_of_rows = len(results_array[0])
        for index in range(number_of_rows):
            new_line = None
            for file_results in results_array:
                file_results_line = file_results[index]
                file_results_line = GlobalizeUtils.convert_line(file_results_line)
                new_line = file_results_line if new_line is None else self.__merge_lines(new_line, file_results_line)
            new_lines.append(new_line)
        assert(len(new_lines) == number_of_rows)
        return new_lines

    @staticmethod
    def __merge_lines(line1, line2):
        CSVConstants.check_lines(line1, line2)

        for index in range(len(line1)):
            if CSVConstants.is_percentage_index(index):
                pass
            elif isinstance(line1[index], int):
                line1[index] += line2[index]
        return line1

    def __results_array(self, dataset_name, filenames, change_index):
        self.input_file.find_dataset(dataset_name)
        results = []
        for filename in filenames:
            self.input_file.find_filename(filename)
            filename_results = ResultsReader.add_until_change(self.input_file, change_index)
            results.append(filename_results)
        assert(len(results) == len(filenames))
        return results


def run(value):
    print "run(" + str(value) + ")"
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-18"
    output_file = "complete-mask-mode=" + str(value) + "-global.csv"
    GlobalizeResults(value, output_path, output_file)

run(0)
run(3)
