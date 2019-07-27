import sys
sys.path.append('.')

from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils


#
# This script does the same as avances11/process_results.py but using pandas data handling.
#
class ProcessResults(object):
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderFR', 'CoderSF',
                    'CoderGAMPS', 'CoderGAMPSLimit']
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
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/data_analysis/"

    def __init__(self, global_mode):
        self.global_mode = global_mode
        if self.global_mode:
            self.df = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
        else:
            self.df = ResultsToDataframe(ResultsReader('raw', 3)).create_full_df()

        self.csv_writer_1, self.csv_writer_2 = None, None
        self.panda_utils = None
        self.dataset_name = None
        self.filename = None
        self.col_index, self.col_name = None, None
        self.__process_results()

    def __process_results(self):
        self.__write_headers()
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            print self.dataset_name
            self.csv_writer_1.write_row([self.dataset_name])
            self.csv_writer_2.write_row([self.dataset_name])
            self.__dataset_results()

    def __write_headers(self):
        extra_str = '-global.csv' if self.global_mode else '-local.csv'
        self.csv_writer_1 = CSVWriter(ProcessResults.PATH, 'process1' + extra_str)
        self.csv_writer_2 = CSVWriter(ProcessResults.PATH, 'process2' + extra_str)

        row = ["Dataset", "Filename", "Column", "Coder"] + ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS
        self.csv_writer_1.write_row(row)

        self.csv_writer_2.write_row(["Dataset", "Filename", "Column"] + ProcessResults.thresholds_array())
        self.csv_writer_2.write_row([None, None, None] + ProcessResults.second_line())

    def __dataset_results(self):
        dataset_filenames = ExperimentsUtils.dataset_csv_filenames(self.dataset_name)
        if self.global_mode and len(dataset_filenames) > 1:
            dataset_filenames = ['Global']

        for self.filename in dataset_filenames:
            print self.filename
            self.csv_writer_1.write_row(['', self.filename])
            self.csv_writer_2.write_row(['', self.filename])
            self.__filename_results()

    def __filename_results(self):
        self.panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, 3)
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ProcessResults.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            print self.col_name
            self.csv_writer_1.write_row(['', '', self.col_name])
            self.__column_results()

    def __column_results(self):
        threshold_results = [None, None, self.col_name]
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(None, self.col_index, threshold)
            coder_name = row_df['coder']
            window = int(row_df['window'])
            percentage = self.__parse_percentage(row_df)
            threshold_results += ['', coder_name, window, percentage]

        self.csv_writer_2.write_row(threshold_results)

        for self.coder_name in ProcessResults.CODERS_ARRAY:
            print self.coder_name
            self.__coder_results()

    def __coder_results(self):
        windows, percentages = [], []
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(self.coder_name, self.col_index, threshold)
            window = int(row_df['window'])
            percentage = self.__parse_percentage(row_df)

            windows.append(window)
            percentages.append(percentage)

        self.csv_writer_1.write_row(['', '', '', self.coder_name] + windows + [''] + percentages)

    def __parse_percentage(self, row_df):
        percentage_key = ResultsToDataframe.percentage_column_key(self.col_index)
        return round(row_df[percentage_key], 2)

    @staticmethod
    def thresholds_array():
        array = []
        for threshold in ExperimentsUtils.THRESHOLDS:
            array += [None, None, str(threshold) + " (%)", None]
        return array

    @staticmethod
    def second_line():
        array = []
        for _ in ExperimentsUtils.THRESHOLDS:
            array += [None, "Coder", "Win", "CR (%)"]
        return array

ProcessResults(True)
ProcessResults(False)
