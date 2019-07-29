import sys
sys.path.append('.')

from auxi.os_utils import python_project_path
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.math_utils import MathUtils
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.data_analysis.process_results import ProcessResults, Writer2
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils


#
# This script is used to compare the results obtained from PCA and APCA coders
#
class PCAvsAPCA(object):
    PATH = python_project_path() + "/scripts/informe/data_analysis/out_apca_vs_pca"

    def __init__(self):
        self.debug_mode = True
        self.output = CSVWriter(PCAvsAPCA.PATH, 'pca_vs_apca.csv')

        self.results_reader = ResultsReader('global', ProcessResults.MM)
        self.df = ResultsToDataframe(self.results_reader).create_full_df()

        # self.results_reader_raw_0 = ResultsReader('raw_basic', 0)
        self.results_reader_raw_3 = ResultsReader('raw_basic', 3)
        # self.df_raw_0 = ResultsToDataframe(self.results_reader_raw_0).create_full_df()
        self.df_raw_3 = ResultsToDataframe(self.results_reader_raw_3).create_full_df()

    def run(self):
        self.output.write_row(Writer2.first_row())
        self.output.write_row(Writer2.second_row())
        self.__datasets_iteration()

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            print self.dataset_name
            self._print(self.dataset_name)
            self.output.write_row([self.dataset_name])
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
            self.__coder_results('CoderAPCA', True)
            self.__coder_results('CoderPCA')
            self.__optimal_pca_results()

    #
    # Get the best <Coder, Window> combination for each <Column, Threshold> combination
    #
    def __coder_results(self, coder_name, first_row=False):
        threshold_results = [None, None, self.col_name if first_row else None]
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(coder_name, self.col_index, threshold)
            window, percentage, coder_name = ProcessResults.get_values(row_df, self.col_index)
            threshold_results += [coder_name.replace("Coder", ""), window, percentage]
        self.output.write_row(threshold_results)

    def __optimal_pca_results(self):
        threshold_results = [None, None, None]
        for threshold in ExperimentsUtils.THRESHOLDS:
            windows = []
            # TODO: move this logic to panda utils
            total_pca, total_basic = 0, 0
            for filename in ExperimentsUtils.dataset_csv_filenames(self.dataset_name):
                data_column_key = ResultsToDataframe.data_column_key(self.col_index)

                # panda_utils_0 = PandasUtils(self.dataset_name, filename, self.df_raw_0, 0)


                panda_utils_3 = PandasUtils(self.dataset_name, filename, self.df_raw_3, 3)
                pca_df = panda_utils_3.min_value_for_threshold('CoderPCA', self.col_index, threshold)

                basic_df = panda_utils_3.coder_basic_df()
                total_basic += basic_df[data_column_key]

                total_pca += pca_df[data_column_key]
                windows.append(pca_df['window'])

            windows = [int(window) for window in windows]
            percentage = MathUtils.calculate_percentage(total_basic, total_pca, 2)
            threshold_results += ["PCA-O", str(windows), percentage]
        self.output.write_row(threshold_results)

    def _print(self, value):
        if self.debug_mode:
            print value


def run():
    PCAvsAPCA().run()

run()
