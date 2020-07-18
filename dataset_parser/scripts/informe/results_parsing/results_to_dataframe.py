import sys
sys.path.append('.')

import pandas as pd

from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.math_utils import MathUtils


class ResultsToDataframe(object):
    DATA_COLUMN_PREFIX = 'column_'
    PERCENTAGE_PREFIX = 'percentage_'
    KEY_TO_INDEX = {
        'dataset': CSVConstants.INDEX_DATASET,
        'filename': CSVConstants.INDEX_FILENAME,
        'coder': CSVConstants.INDEX_ALGORITHM,
        'threshold': CSVConstants.INDEX_THRESHOLD,
        'window': CSVConstants.INDEX_WINDOW
    }

    def __init__(self, results_reader):
        self.results_reader = results_reader

    def create_full_df(self, gzip_results_reader=None):
        lines = self.results_reader.full_results()
        df = self.__create_df(lines)

        if gzip_results_reader is not None:
            gzip_df = self.__create_gzip_df(df, gzip_results_reader)
            df = df.append(gzip_df, ignore_index = True)

        # print df['dataset'].unique()
        # print df['filename'].unique()
        return df

    def create_dataset_df(self, dataset_name):
        lines = self.results_reader.dataset_results(dataset_name)
        df = self.__create_df(lines)
        assert(df['dataset'].unique() == [dataset_name])
        # print df['filename'].unique()
        return df

    def create_filename_df(self, dataset_name, filename):
        lines = self.results_reader.filename_results(dataset_name, filename)
        df = self.__create_df(lines)
        assert(df['dataset'].unique() == [dataset_name])
        assert(df['filename'].unique() == [filename])
        return df

    @staticmethod
    def data_column_key(count):
        return ResultsToDataframe.DATA_COLUMN_PREFIX + str(count)

    @staticmethod
    def percentage_column_key(count):
        return ResultsToDataframe.PERCENTAGE_PREFIX + str(count)

    ####################################################################################################################

    @staticmethod
    def __create_gzip_df(df, gzip_results_reader):
        converted_lines = []
        dataset_pairs = df[['dataset','filename']].drop_duplicates()
        for index, row in dataset_pairs.iterrows():
            new_line = ResultsToDataframe.__gzip_new_line(gzip_results_reader, row)
            for threshold in ExperimentsUtils.THRESHOLDS:  # add one row for every threshold
                threshold_line = new_line.copy()
                threshold_line[4] = threshold
                converted_lines.append(threshold_line)
        gzip_df = ResultsToDataframe.__create_df_aux(converted_lines)
        return gzip_df

    @staticmethod
    def __gzip_new_line(gzip_results_reader, row):
        dataset_name, filename = row
        new_line = [dataset_name, filename, None, 'CoderGZIP'] + [None] * 9
        for column_name in ExperimentsUtils.COLUMN_INDEXES[dataset_name]:
            gzip_bits, base_bits = gzip_results_reader.gzip_and_base_bits(dataset_name, filename, column_name)
            percentage = MathUtils.calculate_percentage(base_bits, gzip_bits, 5)
            new_line += [gzip_bits, 0, gzip_bits, percentage]
        return new_line

    ####################################################################################################################

    @staticmethod
    def __create_df(lines):
        converted_lines = ResultsReader.convert_lines(lines)
        df = ResultsToDataframe.__create_df_aux(converted_lines)
        return df

    @staticmethod
    def __create_df_aux(converted_lines):
        data = ResultsToDataframe.__create_data(converted_lines)
        df = pd.DataFrame(data)
        return df

    @staticmethod
    def __create_data(converted_lines):
        data_obj, current = {}, {}
        for key in ResultsToDataframe.KEY_TO_INDEX.keys():
            data_obj[key], current[key] = [], None

        max_length = len(max(converted_lines, key=len))

        for line in converted_lines:
            ResultsToDataframe.__update_current(current, line)
            ResultsToDataframe.__append_current(data_obj, current)
            ResultsToDataframe.__append_columns(data_obj, line, max_length)
        return data_obj

    @staticmethod
    def __update_current(current, line):
        for key in current.keys():
            index = ResultsToDataframe.KEY_TO_INDEX[key]
            current[key] = line[index] or current[key]

        if line[CSVConstants.INDEX_THRESHOLD] == 0:
            current['threshold'] = 0

    @staticmethod
    def __append_current(data_obj, current):
        for key in current.keys():
            data_obj[key].append(current[key])

    @staticmethod
    def __append_columns(data_obj, line, max_length):
        count = 1
        for index in range(max_length):
            if CSVConstants.is_column_index(index):
                key = ResultsToDataframe.__check_key(data_obj, count, ResultsToDataframe.DATA_COLUMN_PREFIX)
                data_obj[key].append(line[index] if index < len(line) else None)
            elif CSVConstants.is_column_percentage_index(index):
                key = ResultsToDataframe.__check_key(data_obj, count, ResultsToDataframe.PERCENTAGE_PREFIX)
                data_obj[key].append(line[index] if index < len(line) else None)
                count += 1

    @staticmethod
    def __check_key(data_obj, count, string):
        key = string + str(count)
        if key not in data_obj.keys():
            data_obj[key] = []
        return key
