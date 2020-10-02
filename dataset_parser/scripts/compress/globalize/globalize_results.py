import sys
sys.path.append('.')

import filecmp

from scripts.compress.experiments_utils import ExperimentsUtils
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.globalize.globalize_utils import GlobalizeUtils
from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_paths import ResultsPaths

#
# Converts the results in "complete-mask-mode=N.csv" files so that the results of multiple files are merged
#
class GlobalizeResults(object):
    NUMBER_OF_ROWS = {"NM": 393, "M": 457}

    def __init__(self, mask_mode):
        if mask_mode not in ["NM", "M"]:
            print("mask_mode = " + str(mask_mode))
            raise(ValueError, "ERROR: invalid parameters")

        self.mask_mode = mask_mode
        self.number_of_rows = GlobalizeResults.NUMBER_OF_ROWS[mask_mode]

        self.results_reader = ResultsReader('local', mask_mode)

        output_path, output_filename = ResultsPaths.get_path_and_filename('global', mask_mode)
        self.output_file = CSVWriter(output_path, output_filename)
        self.output_file.write_row(self.results_reader.read_line_no_count())

    def run(self):
        for dataset_obj in ExperimentsUtils.DATASETS_ARRAY:
            self.__globalize_dataset(dataset_obj['name'])

    def __globalize_dataset(self, dataset_name):
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset_name)
        if len(filenames) == 1:
            print(dataset_name + " - single file")
            self.multiple_files = False
        else:
            print(dataset_name + " - multiple files")
            self.multiple_files = True
        self.__merge_results(dataset_name, filenames)

    #
    # globalize results
    #
    def __merge_results(self, dataset_name, filenames):
        # MM=0 => CoderBase
        coder_base_line = self.__get_coder_base_line(dataset_name, filenames)
        coder_base_line_with_percentages = ResultsReader.set_percentages(coder_base_line, coder_base_line)
        self.output_file.write_row(coder_base_line_with_percentages)

        # MM=0or3 => CoderBase, CoderPCA, CoderAPCA, etc.
        other_coders_lines = self.__get_other_coders_lines(dataset_name, filenames)
        GlobalizeUtils.write_other_coders_lines(self.output_file, coder_base_line, other_coders_lines)

    def __get_coder_base_line(self, dataset_name, filenames):
        results_array_0 = self.__results_array(dataset_name, filenames, CSVConstants.INDEX_ALGORITHM)
        assert(len(results_array_0[0]) == 1)
        return self.__mask_results_lines(results_array_0)[0]

    def __get_other_coders_lines(self, dataset_name, filenames):
        results_array = self.__results_array(dataset_name, filenames)
        # print len(results_array[0])
        assert(len(results_array[0]) == self.number_of_rows)
        return self.__mask_results_lines(results_array)

    def __mask_results_lines(self, results_array):
        new_lines = []
        number_of_rows = len(results_array[0])
        for index in range(number_of_rows):
            new_line = None
            for file_results in results_array:
                # print file_results
                file_results_line = file_results[index]
                file_results_line = GlobalizeUtils.convert_line(file_results_line, self.multiple_files)
                new_line = file_results_line if new_line is None else self.__merge_lines(new_line, file_results_line)
            new_lines.append(new_line)
        assert(len(new_lines) == number_of_rows)
        return new_lines

    @staticmethod
    def __merge_lines(line1, line2):
        CSVConstants.check_lines(line1, line2)
        skip_index = [CSVConstants.INDEX_WINDOW, CSVConstants.INDEX_THRESHOLD]
        for index in range(len(line1)):
            if CSVConstants.is_percentage_index(index) or index in skip_index:
                pass
            elif isinstance(line1[index], int):
                line1[index] += line2[index]
        return line1

    def __results_array(self, dataset_name, filenames, change_index=CSVConstants.INDEX_FILENAME):
        results = []
        for filename in filenames:
            filename_results = self.results_reader.filename_results(dataset_name, filename, change_index)
            results.append(filename_results)
        assert(len(results) == len(filenames))
        return results

    @staticmethod
    def compare_files(path_1, filename_1, path2, filename_2):
        compare = filecmp.cmp(path_1 + "/" + filename_1, path2 + "/" + filename_2)
        if compare:
            print("SAME!")
        assert compare
