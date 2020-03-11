import sys
sys.path.append('.')

from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.data_analysis.threshold_compare import ThresholdCompare
from scripts.informe.data_analysis.process_results.writer1 import Writer1
from scripts.informe.data_analysis.process_results.writer2 import Writer2
from scripts.informe.data_analysis.process_results.writer_latex import WriterLatex


#
# This script does the same as avances11/process_results.py but using pandas data handling.
#
class ProcessResults(object):
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderFR', 'CoderSF',
                    # 'CoderGAMPS', => ignore this coder
                    'CoderGAMPSLimit']
    MM = 3  # MASK MODE
    DEBUG_MODE = False

    #
    # mode=1 => consider every algorithm
    # mode=2 => consider every algorithm + gzip
    # mode=3 => only consider the PCA algorithm
    # mode=4 => only consider the APCA algorithm
    #
    def __init__(self, global_mode, path, mode):
        # set script settings
        self.global_mode = global_mode
        self.path = path
        self.mode = mode

        # set other instances
        key = 'global' if self.global_mode else 'raw_basic'
        self.results_reader = ResultsReader(key, ProcessResults.MM)
        self.df = ResultsToDataframe(self.results_reader).create_full_df()
        self.threshold_compare = ThresholdCompare(ResultsReader('raw', ProcessResults.MM))

    def run(self):
        self.__write_headers()
        self.__datasets_iteration()
        self.csv_writer_latex.print_end()

    def __write_headers(self):
        extra_str = 'global' if self.global_mode else 'local'
        self.csv_writer_1 = Writer1.filename(self.path, extra_str)
        self.csv_writer_1.write_row(Writer1.first_row())

        self.csv_writer_2 = Writer2.filename(self.path, extra_str)
        self.csv_writer_2.write_row(Writer2.first_row())
        self.csv_writer_2.write_row(Writer2.second_row())

        self.csv_writer_latex = WriterLatex(self.path, extra_str, self.mode)

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            print(self.dataset_name)
            self._print(self.dataset_name)
            self.__set_dataset(self.dataset_name)
            self.__filenames_iteration()

    def __filenames_iteration(self):
        dataset_filenames = ProcessResults.dataset_filenames(self.dataset_name, self.global_mode)
        for self.filename in dataset_filenames:
            self._print(self.filename)
            self.__set_filename(self.filename)
            self.__columns_iteration()

    def __columns_iteration(self):
        self.panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, ProcessResults.MM)
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            if self.__local_or_single_file():
                self.threshold_compare.calculate_matching_thresholds(self.dataset_name, self.filename, self.col_index)
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self._print(self.col_name)
            self.__column_results_writer_1()
            self.__column_results_writer_2()

    def __column_results_writer_1(self):
        self.csv_writer_1.write_row(['', '', self.col_name])
        for self.coder_name in self.__coders_array():
            self._print(self.coder_name)
            self.__coder_results()

    def __coders_array(self):
        if self.mode == 3:
            return ['CoderPCA']
        if self.mode == 4:
            return ['CoderAPCA']
        return ProcessResults.CODERS_ARRAY

    #
    # Get the best Window for each <Coder, Column, Threshold> combination
    #
    def __coder_results(self):
        windows, percentages = [], []
        previous_window, previous_percentage = None, None
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(self.coder_name, self.col_index, threshold)
            window, percentage, _ = ProcessResults.get_values(row_df, self.col_index)

            new_window, new_percentage = window, percentage
            if self.__same_result(threshold):
                assert(threshold > 0); assert(window == previous_window); assert(percentage == previous_percentage)
                # TODO: uncomment to show blank cells for a repeated experiment
                # new_window, new_percentage = '=', '='
            elif self.coder_name == 'CoderSF':
                new_window = ''  # CoderSF this coder doesn't have a window param

            windows.append(new_window); percentages.append(new_percentage)
            previous_window, previous_percentage = window, percentage

        self.csv_writer_1.write_row(['', '', '', self.coder_name] + windows + [''] + percentages)

    #
    # Get the best <Coder, Window> combination for each <Column, Threshold> combination
    #
    def __column_results_writer_2(self):
        coder = self.__coder()
        previous_coder, previous_window, previous_percentage = None, None, None
        threshold_results = [None, None, self.col_name]
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(coder, self.col_index, threshold)
            window, percentage, coder_name = ProcessResults.get_values(row_df, self.col_index)
            coder_name = coder_name.replace("Coder", "")

            new_coder, new_window, new_percentage = coder_name, window, percentage
            if self.__same_result(threshold):
                assert(threshold > 0); assert(coder_name == previous_coder); assert(window == previous_window);
                assert(percentage == previous_percentage)
                # TODO: uncomment to show blank cells for a repeated experiment
                # new_coder, new_window, new_percentage = '=', '=', '='

            threshold_results += [new_coder, new_window, new_percentage]
            previous_coder, previous_window, previous_percentage = coder_name, window, percentage
        self.csv_writer_2.write_row(threshold_results)
        self.csv_writer_latex.set_threshold_results(threshold_results)

    def __coder(self):
        if self.mode == 3:
            return 'CoderPCA'
        if self.mode == 4:
            return 'CoderAPCA'
        return None

    def __set_dataset(self, dataset_name):
        self.__write_two_files([dataset_name])
        self.csv_writer_latex.set_dataset(dataset_name)

    def __set_filename(self, filename):
        self.__write_two_files(['', filename])
        self.csv_writer_latex.set_filename(filename)

    def __write_two_files(self, row):
        self.csv_writer_1.write_row(row)
        self.csv_writer_2.write_row(row)

    def __local_or_single_file(self):
        condition1 = not self.global_mode
        condition2 = self.global_mode and self.__single_file_dataset()
        return condition1 or condition2

    def __same_result(self, threshold):
        return self.__local_or_single_file() and self.threshold_compare.matching_threshold(threshold)

    def __single_file_dataset(self):
        return ExperimentsUtils.dataset_csv_files_count(self.dataset_name) == 1

    def _print(self, value):
        if self.DEBUG_MODE:
            print(value)

    @staticmethod
    def get_values(row_df, col_index):
        window = int(row_df['window'])
        percentage = ProcessResults.parse_percentage(row_df, col_index)
        coder_name = row_df['coder']
        return window, percentage, coder_name

    @staticmethod
    def parse_percentage(row_df, col_index):
        percentage_key = ResultsToDataframe.percentage_column_key(col_index)
        return round(row_df[percentage_key], 2)

    @staticmethod
    def dataset_filenames(dataset_name, global_mode):
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset_name)
        return ['Global'] if global_mode and len(filenames) > 1 else filenames
