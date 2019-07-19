import sys
sys.path.append('.')

import numpy as np
import pandas as pd
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_to_pandas import ResultsToPandas


class PandasUtils(object):
    NUMBER_OF_COMBINATIONS = len(ExperimentsUtils.THRESHOLDS) * len(ExperimentsUtils.WINDOWS)
    FIXED_ROWS = ['coder', 'threshold', 'window']
    MAX_DIFF = 0.009

    def __init__(self, dataset_name, df, mask_mode):
        assert(mask_mode in [0, 3])
        self.dataset_name = dataset_name
        self.df = df
        self.mask_mode = mask_mode
        self.data_columns_count = PandasUtils.__calculate_data_columns_count(df)
        self.__check_df()
        self.__calculate_percentage()

    @staticmethod
    def __calculate_data_columns_count(df):
        data_columns_count = (len(df.columns) - len(PandasUtils.FIXED_ROWS)) / 2
        return data_columns_count

    def __check_df(self):
        # check that the number of data columns is ok
        assert(self.data_columns_count == ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name))

        # check that data for every coder is included
        coders = self.df['coder'].unique()
        expected_coders = ExperimentsUtils.CODERS_NO_MASK_MODE if self.mask_mode == 0 else ExperimentsUtils.CODERS
        np.testing.assert_array_equal(coders, expected_coders)

        # check that the rows count for each coder match
        for coder_name in coders:
            self.__check_coder_rows_count(coder_name)

    def __check_coder_rows_count(self, coder_name):
        rows_count = self.__coder_rows_count(coder_name)
        if coder_name == 'CoderBasic':
            assert(rows_count == 1)
        elif coder_name == 'CoderSF':
            assert(rows_count == len(ExperimentsUtils.THRESHOLDS))
        else:
            # the rest of the coders have the same number of rows
            if rows_count != self.NUMBER_OF_COMBINATIONS:
                print self.__coder_df(coder_name)
                print coder_name
                print rows_count
                assert(rows_count == self.NUMBER_OF_COMBINATIONS)

    def __coder_rows_count(self, coder_name):
        rows_count, _ = self.__coder_df(coder_name).shape
        return rows_count

    def __coder_df(self, coder_name):
        return self.df.loc[self.df['coder'] == coder_name]

    def __calculate_percentage(self):
        for value in range(1, self.data_columns_count + 1):  # [1, ... ]
            data_col_key = ResultsToPandas.data_column_key(value)
            percentage_col_key = ResultsToPandas.percentage_column_key(value)

            basic_coder_total = self.__coder_df("CoderBasic")[data_col_key].iloc[0]
            new_percentage_col_key = 'new_' + percentage_col_key
            self.df[new_percentage_col_key] = 100 * (self.df[data_col_key] / basic_coder_total)

            self.__check_difference(percentage_col_key, new_percentage_col_key)

            # rename percentages column
            self.df.rename(columns={new_percentage_col_key: percentage_col_key}, inplace=True)

    def __check_difference(self, percentage_col_key, new_percentage_col_key):
        # check that the difference between the values is small (< self.MAX_DIFF)
        aux_percentage_col_key = 'aux_' + percentage_col_key
        self.df[aux_percentage_col_key] = self.df[new_percentage_col_key] - self.df[percentage_col_key]
        max_absolute_value = self.df[aux_percentage_col_key].abs().max()
        assert(max_absolute_value < self.MAX_DIFF)
        # remove aux columns
        del self.df[percentage_col_key]
        del self.df[aux_percentage_col_key]

    ####################################################################################################################

    def min_value_for_every_coder(self, coders_array, column_index):
        new_df = pd.DataFrame(columns=self.df.columns)
        for coder_name in coders_array:
            df = self.min_value_for_each_threshold(coder_name, column_index)
            new_df = new_df.append(df, ignore_index=True)
        return new_df

    def min_value_for_each_threshold(self, coder_name, column_index):
        data_column_key = ResultsToPandas.data_column_key(column_index)
        coder_df = self.__coder_df(coder_name)
        new_df = pd.DataFrame(columns=self.df.columns)
        for index, threshold in enumerate(ExperimentsUtils.THRESHOLDS):
            new_df.loc[index] = self.get_min_row(coder_df, data_column_key, threshold)
        return new_df

    #
    # Given a coder_df, a column_key, and a threshold:
    # it returns the row with the minimum value for that column for that <coder, threshold> combination
    #
    @staticmethod
    def get_min_row(coder_df, column_key, threshold):
        threshold_df = coder_df.loc[coder_df['threshold'] == threshold]
        min_value_index = threshold_df[column_key].argmin()
        min_value = threshold_df.loc[min_value_index][column_key]

        min_value_rows_count = threshold_df[threshold_df[column_key] == min_value].count()[column_key]
        assert(min_value_rows_count == 1)

        min_value_row = threshold_df.loc[min_value_index]
        return min_value_row.values
