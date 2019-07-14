import sys
sys.path.append('.')

import numpy as np
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_to_pandas import ResultsToPandas


class PandasUtils(object):
    NUMBER_OF_COMBINATIONS = len(ExperimentsUtils.THRESHOLDS) * len(ExperimentsUtils.WINDOWS)
    FIXED_ROWS = ['coder', 'threshold', 'window']
    MAX_DIFF = 0.009

    def __init__(self, dataset_name, df):
        self.dataset_name = dataset_name
        self.df = df
        self.data_columns_count = PandasUtils.__calculate_data_columns_count(df)
        self.__check_df()
        self.__calculate_percentage()
        # print self.df

    @staticmethod
    def __calculate_data_columns_count(df):
        data_columns_count = (len(df.columns) - len(PandasUtils.FIXED_ROWS)) / 2
        return data_columns_count

    def __check_df(self):
        # check that the number of data columns is ok
        assert(self.data_columns_count == ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name))

        # check that data for every coder is included
        coders = self.df['coder'].unique()
        np.testing.assert_array_equal(coders, ExperimentsUtils.CODERS)

        for coder in coders:
            self.__check_coder_rows_count(coder)

    def __check_coder_rows_count(self, coder):
        rows, _ = self.df.loc[self.df['coder'] == coder].shape
        if coder == 'CoderBasic':
            assert(rows == 1)
        elif coder == 'CoderSF':
            assert(rows == len(ExperimentsUtils.THRESHOLDS))
        else:
            # the rest of the coders have the same number of rows
            assert(rows == self.NUMBER_OF_COMBINATIONS)

    def __calculate_percentage(self):
        for value in range(1, self.data_columns_count + 1):  # [1, ... ]
            data_col_key = ResultsToPandas.data_column_key(value)
            percentage_col_key = ResultsToPandas.percentage_column_key(value)

            new_percentage_col_key = 'new_' + percentage_col_key
            aux_percentage_col_key = 'aux_' + percentage_col_key

            basic_coder_total = self.df.loc[self.df['coder'] == "CoderBasic"][data_col_key].iloc[0]
            self.df[new_percentage_col_key] = 100 * (self.df[data_col_key] / basic_coder_total)

            # check that the difference between the values is small
            self.df[aux_percentage_col_key] = self.df[new_percentage_col_key] - self.df[percentage_col_key]
            max_absolute_value = self.df[aux_percentage_col_key].abs().max()
            assert(max_absolute_value < self.MAX_DIFF)

            # remove aux columns and keep the calculated values
            del self.df[percentage_col_key]
            del self.df[aux_percentage_col_key]
            self.df.rename(columns={new_percentage_col_key: percentage_col_key})

        print self.df

