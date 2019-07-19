import sys
sys.path.append('.')

import numpy as np
import pandas as pd
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe


class PandasUtils(object):
    FIXED_ROWS = ResultsToDataframe.KEY_TO_INDEX.keys()
    MAX_DIFF = 0.009

    def __init__(self, dataset_name, filename, df, mask_mode):
        assert(mask_mode in [0, 3])

        self.df = self.filename_df(df, dataset_name, filename)
        self.mask_mode = mask_mode

        self.data_columns_count = (len(self.df.columns) - len(PandasUtils.FIXED_ROWS)) / 2
        PandasUtilsCheck(self).check_df(dataset_name)
        self.__calculate_percentage()

    @staticmethod
    def filename_df(df, dataset_name, filename):
        df = df.loc[(df['dataset'] == dataset_name) & (df['filename'] == filename)]
        df = df.dropna(axis=1, how='all')  # drop the columns where all elements are NaN:
        return df

    @staticmethod
    def coder_df(df, coder_name):
        return df.loc[df['coder'] == coder_name]

    @staticmethod
    def threshold_df(df, threshold):
        return df.loc[df['threshold'] == threshold]

    def __calculate_percentage(self):
        for value in range(1, self.data_columns_count + 1):  # [1, ... ]
            data_col_key = ResultsToDataframe.data_column_key(value)
            percentage_col_key = ResultsToDataframe.percentage_column_key(value)
            new_percentage_col_key = 'new_' + percentage_col_key

            basic_coder_total = self.coder_df(self.df, "CoderBasic")[data_col_key].iloc[0]
            self.df[new_percentage_col_key] = 100 * (self.df[data_col_key] / basic_coder_total)
            self.__check_difference(percentage_col_key, new_percentage_col_key)

            # rename percentages column
            self.df.rename(columns={new_percentage_col_key: percentage_col_key}, inplace=True)

    #
    # Check that the difference between the csv percentage and the
    # percentage calculated by pandas is small (< self.MAX_DIFF)
    #
    def __check_difference(self, percentage_col_key, new_percentage_col_key):
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
        data_column_key = ResultsToDataframe.data_column_key(column_index)
        coder_df = self.coder_df(self.df, coder_name)
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
        threshold_df = PandasUtils.threshold_df(coder_df, threshold)
        min_value_index = threshold_df[column_key].argmin()
        min_value = threshold_df.loc[min_value_index][column_key]

        min_value_rows_count = threshold_df[threshold_df[column_key] == min_value].count()[column_key]
        assert(min_value_rows_count == 1)

        min_value_row = threshold_df.loc[min_value_index]
        return min_value_row.values


class PandasUtilsCheck(object):
    NUMBER_OF_COMBINATIONS = len(ExperimentsUtils.THRESHOLDS) * len(ExperimentsUtils.WINDOWS)

    def __init__(self, pandas_utils):
        self.pandas_utils = pandas_utils
        self.df = pandas_utils.df
        self.mask_mode = pandas_utils.mask_mode
        self.data_columns_count = pandas_utils.data_columns_count
        
    def check_df(self, dataset_name):
        # check that the number of data columns is ok
        assert(self.data_columns_count == ExperimentsUtils.get_dataset_data_columns_count(dataset_name))

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
                print PandasUtils.coder_df(self.df, coder_name)
                print coder_name
                print self.NUMBER_OF_COMBINATIONS
                print rows_count
                assert(rows_count == self.NUMBER_OF_COMBINATIONS)
    
    def __coder_rows_count(self, coder_name):
        rows_count, _ = PandasUtils.coder_df(self.df, coder_name).shape
        return rows_count
