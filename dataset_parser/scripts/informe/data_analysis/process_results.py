import sys
sys.path.append('.')

from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.data_analysis.threshold_compare import ThresholdCompare


#
# This script does the same as avances11/process_results.py but using pandas data handling.
#
class ProcessResults(object):
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderFR', 'CoderSF',
                    # 'CoderGAMPS', => ignore this coder
                    'CoderGAMPSLimit']
    COLUMN_INDEXES = {
        'IRKIS': ['VWC'],
        'NOAA-SST': ['SST'],
        'NOAA-ADCP': ['Vel'],
        'SolarAnywhere': ['GHI', 'DNI', 'DHI'],
        'ElNino': ['Lat', 'Long', 'Zonal Winds', 'Merid. Winds', 'Humidity', 'AirTemp', 'SST'],
        'NOAA-SPC-hail': ['Lat', 'Long', 'Size'],
        'NOAA-SPC-tornado': ['Lat', 'Long'],
        'NOAA-SPC-wind': ['Lat', 'Long', 'Speed']
    }
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/data_analysis/results"

    def __init__(self, global_mode):
        self.debug_mode = False
        self.global_mode = global_mode
        if self.global_mode:
            self.results_reader = ResultsReader('global', 3)
        else:
            self.results_reader = ResultsReader('raw', 3)

        self.df = ResultsToDataframe(self.results_reader).create_full_df()
        self.threshold_compare = ThresholdCompare(ResultsReader('raw', 3))
        self.__process_results()

    def __process_results(self):
        self.__write_headers()
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            print self.dataset_name
            self._print(self.dataset_name)
            self.csv_writer_1.write_row([self.dataset_name])
            self.csv_writer_2.write_row([self.dataset_name])
            self.__dataset_results()

    def __write_headers(self):
        extra_str = 'global' if self.global_mode else 'local'
        self.csv_writer_1 = CSVWriter(ProcessResults.PATH, extra_str + '-process1.csv')
        self.csv_writer_2 = CSVWriter(ProcessResults.PATH, extra_str + '-process2.csv')

        row = ["Dataset", "Filename", "Column", "Coder"] + ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS
        self.csv_writer_1.write_row(row)

        self.csv_writer_2.write_row(["Dataset", "Filename", "Column"] + ProcessResults.thresholds_array())
        self.csv_writer_2.write_row([None, None, None] + ProcessResults.second_line())

    def __dataset_results(self):
        dataset_filenames = ExperimentsUtils.dataset_csv_filenames(self.dataset_name)
        if self.global_mode and len(dataset_filenames) > 1:
            dataset_filenames = ['Global']

        for self.filename in dataset_filenames:
            self._print(self.filename)
            self.csv_writer_1.write_row(['', self.filename])
            self.csv_writer_2.write_row(['', self.filename])
            self.__filename_results_writer_1()

    def __filename_results_writer_1(self):
        self.panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, 3)
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            if self.__condition():
                self.threshold_compare.calculate_matching_thresholds(self.dataset_name, self.filename, self.col_index)
            self.col_name = ProcessResults.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self._print(self.col_name)
            self.csv_writer_1.write_row(['', '', self.col_name])
            self.__column_results_writer_1()
            self.__column_results_writer_2()

    def __column_results_writer_1(self):
        for self.coder_name in ProcessResults.CODERS_ARRAY:
            self._print(self.coder_name)
            self.__coder_results()

    def __coder_results(self):
        windows, percentages = [], []
        previous_window, previous_percentage = None, None
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(self.coder_name, self.col_index, threshold)
            window = int(row_df['window'])
            percentage = self.__parse_percentage(row_df)

            new_window, new_percentage = window, percentage
            if self.__condition() and self.threshold_compare.matching_threshold(threshold):
                assert(threshold > 0); assert(window == previous_window); assert(percentage == previous_percentage)
                new_window, new_percentage = '=', '='
            elif self.coder_name == 'CoderSF':
                new_window = ''  # CoderSF this coder doesn't have a window param

            windows.append(new_window); percentages.append(new_percentage)
            previous_window, previous_percentage = window, percentage

        self.csv_writer_1.write_row(['', '', '', self.coder_name] + windows + [''] + percentages)

    def __column_results_writer_2(self):
        previous_coder, previous_window, previous_percentage = None, None, None
        threshold_results = [None, None, self.col_name]
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(None, self.col_index, threshold)
            coder_name, window = row_df['coder'], int(row_df['window'])
            coder_name = coder_name.replace("Coder", "")
            percentage = self.__parse_percentage(row_df)

            new_coder, new_window, new_percentage = coder_name, window, percentage
            if self.__condition() and self.threshold_compare.matching_threshold(threshold):
                assert(threshold > 0); assert(coder_name == previous_coder); assert(window == previous_window);
                assert(percentage == previous_percentage)
                new_coder, new_window, new_percentage = '=', '=', '='

            threshold_results += [new_coder, new_window, new_percentage]
            previous_coder, previous_window, previous_percentage = coder_name, window, percentage
        self.csv_writer_2.write_row(threshold_results)

    def __parse_percentage(self, row_df):
        percentage_key = ResultsToDataframe.percentage_column_key(self.col_index)
        return round(row_df[percentage_key], 2)

    def __condition(self):
        condition1 = not self.global_mode
        condition2 = self.global_mode and self.__single_file_dataset()
        return condition1 or condition2

    def __single_file_dataset(self):
        return ExperimentsUtils.dataset_csv_files_count(self.dataset_name) == 1

    @staticmethod
    def thresholds_array():
        array = []
        for threshold in ExperimentsUtils.THRESHOLDS:
            array += [None, str(threshold) + " (%)", None]
        return array

    @staticmethod
    def second_line():
        array = []
        for _ in ExperimentsUtils.THRESHOLDS:
            array += ["Coder", "Win", "CR (%)"]
        return array
    
    def _print(self, value):
        if self.debug_mode:
            print value

ProcessResults(True)
ProcessResults(False)
