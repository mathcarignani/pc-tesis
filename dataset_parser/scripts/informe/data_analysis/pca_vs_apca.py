import sys
sys.path.append('.')

import numpy as np
from auxi.os_utils import OSUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.math_utils import MathUtils
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.data_analysis.process_results.process_results import ProcessResults, Writer2
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.gzip_compare.gzip_results_parser import GzipResultsParser


#
# This script is used to compare the results obtained from PCA and APCA coders
#
class PCAvsAPCA(object):
    PATH = OSUtils.python_project_path() + "/scripts/informe/data_analysis/out_apca_vs_pca"
    GZIP_MODE = True
    THRESHOLD = 30

    def __init__(self):
        self.debug_mode = True
        if self.GZIP_MODE:
            self.output = CSVWriter(PCAvsAPCA.PATH, 'pca_vs_apca_vs_gzip_t_' + str(self.THRESHOLD) + '.csv')
            self.gzip = GZip(self)
        else:
            self.output = CSVWriter(PCAvsAPCA.PATH, 'pca_vs_apca_vs_pca_o.csv')
            self.pca_optimal = PCAOptimalResults(self)

        self.results_reader = ResultsReader('global', ProcessResults.MM)
        self.df = ResultsToDataframe(self.results_reader).create_full_df()

        # self.results_reader_raw_0 = ResultsReader('raw_base', 0)
        self.results_reader_raw_3 = ResultsReader('raw_base', 3) # TODO: this line will fail
        # self.df_raw_0 = ResultsToDataframe(self.results_reader_raw_0).create_full_df()
        self.df_raw_3 = ResultsToDataframe(self.results_reader_raw_3).create_full_df()

    def run(self):
        first_row = Writer2.first_row()
        second_row = Writer2.second_row()
        if self.GZIP_MODE:
            # remove thresholds other than 0
            first_row = first_row[:6]
            second_row = second_row[:6] + ['Rel. diff']
        self.output.write_row(first_row)
        self.output.write_row(second_row)
        self.__datasets_iteration()

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            print self.dataset_name
            self._print(self.dataset_name)
            self.output.write_row([ExperimentsUtils.get_dataset_short_name(self.dataset_name)])
            self.__filenames_iteration()

    def __filenames_iteration(self):
        dataset_filenames = ProcessResults.dataset_filenames(self.dataset_name, True)
        for self.filename in dataset_filenames:
            self._print(self.filename)
            self.output.write_row(['', self.filename])
            self.__columns_iteration()

    def __columns_iteration(self):
        self.panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, ProcessResults.MM)
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self._print(self.col_name)
            apca_results = self.__coder_results('CoderAPCA', True)
            pca_results = self.__coder_results('CoderPCA')
            if self.GZIP_MODE:
                self.gzip.run(apca_results, pca_results)
            else:
                self.pca_optimal.run(apca_results, pca_results)

    #
    # Get the best <Coder, Window> combination for each <Column, Threshold> combination
    #
    def __coder_results(self, coder_name, first_row=False):
        threshold_results = [None, None, self.col_name if first_row else None]
        thresholds = [self.THRESHOLD] if self.GZIP_MODE else ExperimentsUtils.THRESHOLDS
        for threshold in thresholds:
            row_df = self.panda_utils.min_value_for_threshold(coder_name, self.col_index, threshold)
            window, percentage, coder_name = ProcessResults.get_values(row_df, self.col_index)
            threshold_results += [coder_name.replace("Coder", ""), window, percentage]
        return threshold_results

    def _print(self, value):
        if self.debug_mode:
            print value


class PCAOptimalResults(object):
    def __init__(self, apca_vs_pca_instance):
        self.a_vs_a = apca_vs_pca_instance

    def run(self, apca_results, pca_results):
        pca_o_results = self.__pca_optimal_results()
        self.__compare_and_write_results(apca_results, pca_results, pca_o_results)

    def __pca_optimal_results(self):
        threshold_results = [None, None, None]
        for threshold in ExperimentsUtils.THRESHOLDS:
            windows = []
            # TODO: move this logic to panda utils
            total_pca, total_base = 0, 0
            for filename in ExperimentsUtils.dataset_csv_filenames(self.a_vs_a.dataset_name):
                data_column_key = ResultsToDataframe.data_column_key(self.a_vs_a.col_index)

                # panda_utils_0 = PandasUtils(self.dataset_name, filename, self.df_raw_0, 0)
                panda_utils_3 = PandasUtils(self.a_vs_a.dataset_name, filename, self.a_vs_a.df_raw_3, 3)
                pca_df = panda_utils_3.min_value_for_threshold('CoderPCA', self.a_vs_a.col_index, threshold)

                base_df = panda_utils_3.coder_base_df()
                total_base += base_df[data_column_key]
                total_pca += pca_df[data_column_key]
                windows.append(pca_df['window'])

            windows = [int(window) for window in windows]
            percentage = MathUtils.calculate_percentage(total_base, total_pca, 2)
            threshold_results += ["PCA-O", windows, percentage]
        return threshold_results

    def __compare_and_write_results(self, apca_results, pca_results, pca_o_results):
        results_length = len(apca_results)
        assert(len(pca_results) == results_length)
        assert(len(pca_o_results) == results_length)

        new_row = [None] * 3
        single_file = False
        for index in range(len(ExperimentsUtils.THRESHOLDS)):
            coder_index = 3*(index + 1)  # 3, 6, 9, ...
            assert(apca_results[coder_index] == 'APCA')
            assert(pca_results[coder_index] == 'PCA')
            assert(pca_o_results[coder_index] == 'PCA-O')

            # compare PCA and PCA-O windows
            pca_window, pca_o_windows = pca_results[coder_index + 1], pca_o_results[coder_index + 1]
            pca_percentage, pca_o_percentage = pca_results[coder_index + 2], pca_o_results[coder_index + 2]
            apca_percentage = apca_results[coder_index + 2]
            if len(pca_o_windows) == 1:
                single_file = True
                assert(pca_o_windows[0] == pca_window)  # for single files, the windows and percentages should match
                assert(pca_percentage == pca_o_percentage)
                assert(apca_percentage != pca_percentage)
                best = '+APCA' if apca_percentage < pca_percentage else '+PCA'
                relative_difference = MathUtils.relative_difference(pca_percentage, apca_percentage, True)
                new_row += [None, best, relative_difference]

            else:  # len(pca_o_windows) > 1
                unique_windows = np.unique(pca_o_windows)
                if len(unique_windows) == 1:
                    assert(unique_windows[0] == pca_window)
                    assert(pca_percentage == pca_o_percentage)
                    assert(apca_percentage != pca_percentage)
                    best = '+APCA' if apca_percentage < pca_percentage else '+PCA'
                    relative_difference = MathUtils.relative_difference(pca_percentage, apca_percentage, True)
                    new_row += ['SW', best, relative_difference]
                    pca_o_results[coder_index + 2] = None
                else:
                    assert(pca_percentage > pca_o_percentage)
                    assert(apca_percentage != pca_o_percentage)
                    best = '+APCA' if apca_percentage < pca_o_percentage else '+PCA-O'
                    relative_difference = MathUtils.relative_difference(pca_o_percentage, apca_percentage, True)
                    new_row += ['DW', best, relative_difference]

        self.a_vs_a.output.write_row(apca_results)
        self.a_vs_a.output.write_row(pca_results)
        if not single_file:
            self.a_vs_a.output.write_row(pca_o_results)
        self.a_vs_a.output.write_row(new_row)


class GZip(object):
    def __init__(self, apca_vs_pca_instance):
        self.a_vs_a = apca_vs_pca_instance
        # self.gzip_compare = GzipResultsParser()
        self.gzip_compare_t = GzipResultsParser(True)

    def run(self, apca_results, pca_results):
        apca_cr, pca_cr = apca_results[-1], pca_results[-1]
        # gzip_cr = self.gzip_compare.compression_ratio(self.a_vs_a.dataset_name, self.a_vs_a.filename, self.a_vs_a.col_name)
        # gzip_results = [None, None, None, 'GZIP', None, gzip_cr]

        gzip_cr_t = self.gzip_compare_t.compression_ratio(self.a_vs_a.dataset_name, self.a_vs_a.filename, self.a_vs_a.col_name)
        gzip_results_t = [None, None, None, 'GZIP-T', None, gzip_cr_t]

        # best_cr = min([apca_cr, pca_cr, gzip_cr, gzip_cr_t])
        best_cr = min([apca_cr, pca_cr, gzip_cr_t])
        # for array in [apca_results, pca_results, gzip_results, gzip_results_t]:
        for array in [apca_results, pca_results, gzip_results_t]:
            current_cr = array[-1]
            if current_cr != best_cr:
                rel_diff = MathUtils.relative_difference(current_cr, best_cr, True)
                array.append(rel_diff)

        self.a_vs_a.output.write_row(apca_results)
        self.a_vs_a.output.write_row(pca_results)
        # self.a_vs_a.output.write_row(gzip_results)
        self.a_vs_a.output.write_row(gzip_results_t)


def run():
    PCAvsAPCA().run()

run()
