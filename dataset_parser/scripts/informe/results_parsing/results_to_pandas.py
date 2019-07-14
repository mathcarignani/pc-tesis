import sys
sys.path.append('.')

import pandas as pd

from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.results_parsing.results_reader import ResultsReader


class ResultsToPandas(object):
    DATA_COLUMN_PREFIX = 'column_'
    PERCENTAGE_PREFIX = 'percentage_'

    def __init__(self, results_reader):
        self.results_reader = results_reader

    def create_dataframe(self, dataset_name, filename):
        filename_results = self.results_reader.filename_results(dataset_name, filename)
        filename_results = ResultsReader.convert_lines(filename_results)
        data = self.__create_data(filename_results)
        df = pd.DataFrame(data)
        return df

    @staticmethod
    def __create_data(filename_results):
        data_obj = {'coder': [], 'threshold': [], 'window': []}
        current = {'coder': None, 'threshold': None, 'window': None}
        for line in filename_results:
            ResultsToPandas.__update_current(current, line)
            ResultsToPandas.__append_current(data_obj, current)
            ResultsToPandas.__append_columns(data_obj, line)
        return data_obj

    @staticmethod
    def __update_current(current, line):
        current['coder'] = line[CSVConstants.INDEX_ALGORITHM] or current['coder']
        current['threshold'] = line[CSVConstants.INDEX_THRESHOLD] or current['threshold']
        current['window'] = line[CSVConstants.INDEX_WINDOW] or current['window']

    @staticmethod
    def __append_current(data_obj, current):
        for key in ['coder', 'threshold', 'window']:
            data_obj[key].append(current[key])

    @staticmethod
    def __append_columns(data_obj, line):
        count = 1
        for index in range(len(line)):
            if CSVConstants.is_column_index(index):
                key = ResultsToPandas.__check_key(data_obj, count, ResultsToPandas.DATA_COLUMN_PREFIX)
                data_obj[key].append(line[index])
            elif CSVConstants.is_column_percentage_index(index):
                key = ResultsToPandas.__check_key(data_obj, count, ResultsToPandas.PERCENTAGE_PREFIX)
                data_obj[key].append(line[index])
                count += 1

    @staticmethod
    def __check_key(data_obj, count, string):
        key = string + str(count)
        if key not in data_obj.keys():
            data_obj[key] = []
        return key

    @staticmethod
    def data_column_key(count):
        return ResultsToPandas.DATA_COLUMN_PREFIX + str(count)

    @staticmethod
    def percentage_column_key(count):
        return ResultsToPandas.PERCENTAGE_PREFIX + str(count)
