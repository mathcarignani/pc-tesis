import sys
sys.path.append('.')

import pandas as pd
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.data_analysis.threshold_compare import ThresholdCompare
from scripts.informe.data_analysis.process_results.writer1 import Writer1
from scripts.informe.data_analysis.process_results.writer2 import Writer2
from scripts.informe.latex_tables.table_compression.table_compression import TableCompression
from scripts.informe.math_utils import MathUtils
from scripts.informe.gzip_compare.gzip_results_reader import GzipResultsReader


class ProcessResults(object):
    CODERS = ['CoderBase', 'CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderFR', 'CoderSF',
              # 'CoderGAMPS', => ignore this coder
              'CoderGAMPSLimit']
    CODERS_WITHOUT_WINDOW = ['CoderBase', 'CoderSF', 'CoderGZIP']
    MM = "M"  # MASK MODE
    DEBUG_MODE = False

    #
    # mode=1  => best algorithm, considering every algorithm
    # mode=2  => best algorithm, considering every algorithm + gzip
    #
    def __init__(self, global_mode, path, mode, gzip_path=None, gzip_filename=None):
        # set script settings
        self.global_mode = global_mode
        self.path = path
        self.mode = mode
        self.with_gzip = mode == 2

        # set other instances
        self.key = 'global' if self.global_mode else 'local'
        self.results_reader = ResultsReader(self.key, ProcessResults.MM)
        self.df = self.__set_df(gzip_path, gzip_filename)
        self.threshold_compare = ThresholdCompare(ResultsReader('local', ProcessResults.MM))

    def run(self):
        self.__write_headers()
        self.__datasets_iteration()
        self.latex_table.print_end()
        self.csv_writer_1.show_data()

    def __set_df(self, gzip_path, gzip_filename):
        if not self.with_gzip:
            return ResultsToDataframe(self.results_reader).create_full_df()

        assert(self.key == 'global')
        assert gzip_path
        assert gzip_filename
        gzip_results_reader = GzipResultsReader(gzip_path, gzip_filename)
        return ResultsToDataframe(self.results_reader).create_full_df(gzip_results_reader)

    def __write_headers(self):
        extra_str = 'global' if self.global_mode else 'local'
        self.csv_writer_1 = Writer1(self.path, extra_str, self.mode)
        self.csv_writer_2 = Writer2(self.path, extra_str)
        self.latex_table = TableCompression(self.path, self.mode)

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
        self.panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, ProcessResults.MM, True, self.with_gzip)
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            # TODO: uncomment to IGNORE SPEED
            # if self.dataset_name == 'NOAA-SPC-wind' and self.col_index == 3:
            #     continue
            if self.__local_or_single_file():
                self.threshold_compare.calculate_matching_thresholds(self.dataset_name, self.filename, self.col_index)
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self._print(self.col_name)
            self.__column_results_writer_1()
            self.__column_results_writer_2()

    def __column_results_writer_1(self):
        self.csv_writer_1.write_col_name(self.col_name)
        for self.coder_name in self.__coders_array():
            self._print(self.coder_name)
            self.__coder_results()
        self.csv_writer_1.write_data_rows()

    def __coders_array(self):
        coders = ['CoderGZIP'] if self.with_gzip else []
        coders += self.CODERS
        return coders

    #
    # Get the best Window for each <Coder, Column, Threshold> combination
    #
    def __coder_results(self):
        windows, percentages, total_bits_list = [], [], []
        previous_window, previous_percentage, previous_total_bits = None, None, None
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(self.coder_name, self.col_index, threshold)
            window, percentage, _, total_bits = ProcessResults.get_values(row_df, self.col_index)
            new_window, new_percentage, new_total_bits = window, percentage, total_bits

            if self.__same_result(threshold):
                assert(threshold > 0); assert(window == previous_window)
                assert(percentage == previous_percentage); assert(total_bits == previous_total_bits)
                # TODO: uncomment to show blank cells for a repeated experiment
                # new_window, new_percentage, new_total_bits = '=', '=', '=
            elif self.coder_name in self.CODERS_WITHOUT_WINDOW:
                new_window = ''  # these coders don't have a window param

            windows.append(new_window); percentages.append(new_percentage); total_bits_list.append(new_total_bits)
            previous_window, previous_percentage, previous_total_bits = window, percentage, total_bits

        self.csv_writer_1.save_data_row(self.coder_name, windows, percentages, total_bits_list)

    #
    # Get the best <Coder, Window> combination for each <Column, Threshold> combination
    #
    def __column_results_writer_2(self):
        threshold_results = [None, None, self.col_name]
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(None, self.col_index, threshold)
            window, percentage, coder_name, _ = ProcessResults.get_values(row_df, self.col_index)
            coder_name = coder_name.replace("Coder", "")

            new_coder, new_window, new_percentage = coder_name, window, percentage
            threshold_results += [new_coder, new_window, new_percentage]

        self.csv_writer_2.write_row(threshold_results)
        self.latex_table.set_threshold_results(threshold_results)

    def __set_dataset(self, dataset_name):
        self.csv_writer_1.write_dataset_name(dataset_name)
        self.csv_writer_2.write_dataset_name(dataset_name)
        self.latex_table.set_dataset(dataset_name)

    def __set_filename(self, filename):
        self.csv_writer_1.write_filename(filename)
        self.csv_writer_2.write_filename(filename)
        self.latex_table.set_filename(filename)

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
        window = None if pd.isnull(row_df['window']) else int(row_df['window'])
        percentage = ProcessResults.parse_percentage(row_df, col_index)
        total_bits = ProcessResults.parse_total_bits(row_df, col_index)
        coder_name = row_df['coder']
        return window, percentage, coder_name, total_bits

    @staticmethod
    def calculate_relative_diff(row_df_pca, row_df_apca, col_index):
        data_column_key = ResultsToDataframe.data_column_key(col_index)
        size_pca, size_apca = row_df_pca[data_column_key], row_df_apca[data_column_key]
        relative_diff = MathUtils.relative_difference(size_pca, size_apca)
        coder_name = 'PCA' if size_pca < size_apca else 'APCA'
        return round(relative_diff, 2), coder_name

    @staticmethod
    def calculate_RD(row_df_best, row_df_compare, col_index):
        data_column_key = ResultsToDataframe.data_column_key(col_index)
        size_best, size_compare = row_df_best[data_column_key], row_df_compare[data_column_key]
        relative_diff = MathUtils.relative_difference(size_compare, size_best)
        return round(relative_diff, 2)

    @staticmethod
    def parse_percentage(row_df, col_index):
        percentage_key = ResultsToDataframe.percentage_column_key(col_index)
        percentage = round(row_df[percentage_key]/100, 2)
        return percentage

    @staticmethod
    def parse_total_bits(row_df, col_index):
        total_bits_key = ResultsToDataframe.data_column_key(col_index)
        total_bits = row_df[total_bits_key]
        return int(total_bits)

    @staticmethod
    def dataset_filenames(dataset_name, global_mode):
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset_name)
        return ['Global'] if global_mode and len(filenames) > 1 else filenames
