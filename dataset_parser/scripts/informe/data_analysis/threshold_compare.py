import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.csv_constants import CSVConstants
from pandas_tools.pandas_tools import PandasTools


class ThresholdCompare(object):
    #
    # filename can be a filename or 'Global'
    #
    def __init__(self, results_reader):
        self.results_reader = results_reader
        self.matching_thresholds = None

    #
    # Returns an array with the threshold %s for which the values match the values of another threshold %.
    # e.g. when [1, 3, 10] is returned, that means that 1% and 3% match 0% and 10% matches 5%
    #
    def calculate_matching_thresholds(self, dataset_name, filename, col_index):
        column_thresholds = self.__get_column_thresholds(dataset_name, filename, col_index)
        previous_list, previous_threshold = None, None
        self.matching_thresholds = []
        for threshold in ExperimentsUtils.THRESHOLDS:
            if previous_list == column_thresholds[threshold]:
                self.matching_thresholds.append(threshold)
            previous_list = column_thresholds[threshold]

    def matching_threshold(self, threshold):
        return threshold in self.matching_thresholds

    #
    # Returns an object with the thresholds values for every threshold % for a particular column.
    # e.g. { 0: [0, 0, ... , 0],  1: [0, 0, ... , 0],  3: [0, 1, ... , 0],  5: [1, 1, ... , 1],
    #       10: [2, 2, ... , 1], 15: [2, 3, ... , 2], 20: [3, 4, ... , 2], 30: [5, 6, ... , 3]}
    #
    def __get_column_thresholds(self, dataset_name, filename, col_index):
        column_thresholds = {}
        self.results_reader.find_filename_in_dataset(dataset_name, filename)
        columns_count = ExperimentsUtils.get_dataset_data_columns_count(dataset_name)

        # for every threshold percentage, get the threshold values for column with col_index
        for threshold in ExperimentsUtils.THRESHOLDS:
            column_thresholds[threshold] = self.__parse_threshold_list(threshold, col_index, columns_count)
        return column_thresholds

    #
    # For a given threshold percentage (e.g. 0) it returns an array of the threshold values for a particular column
    # (e.g. [0, 0, ... , 0])
    #
    def __parse_threshold_list(self, threshold, col_index, columns_count):
        thresholds_list = self.__read_threshold_list(threshold, columns_count)

        print(col_index)
        print(thresholds_list)
        print(columns_count)

        # only consider the thresholds which are associated to the column with col_index, ignore the rest
        column_thresholds_list = []
        current_index = col_index #- 1  # col_index >= 1, so current_index >= 0
        while current_index < len(thresholds_list):
            current_threshold = thresholds_list[current_index]
            column_thresholds_list.append(current_threshold)
            current_index += columns_count
        print(len(column_thresholds_list))
        print(len(thresholds_list))
        print(columns_count)
        assert(len(column_thresholds_list) == len(thresholds_list) / columns_count)
        return column_thresholds_list

    #
    # Parse the threshold array from the csv.
    #
    def __read_threshold_list(self, threshold, columns_count):
        self.results_reader.find_threshold(threshold)
        line = self.results_reader.line
        assert(int(line[CSVConstants.INDEX_THRESHOLD]) == threshold)
        threshold_list_str = self.results_reader.line[CSVConstants.INDEX_THRESHOLD_LIST]  # '[0, N, 291, 263]'
        thresholds_list = threshold_list_str[1:-1].split(', ')  # ['0', 'N', '291', '263']
        assert(thresholds_list[0] == '0')  # threshold for time column must be 0
        # thresholds_list = thresholds_list[1:]  # ['N', '291', '263'] - remove first '0'
        thresholds_list = [ThresholdCompare.map_value(val) for val in thresholds_list]  # [None, 291, 263]
        assert((len(thresholds_list)-1) % (columns_count-1) == 0)
        return thresholds_list

    @staticmethod
    def map_value(value):
        return None if PandasTools.NO_DATA in value else int(value)
