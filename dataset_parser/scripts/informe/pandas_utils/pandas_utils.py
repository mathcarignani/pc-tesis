import sys
sys.path.append('.')

import pandas as pd
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pandas_utils.pandas_utils_check import PandasUtilsCheck


class PandasUtils(object):
    FIXED_ROWS = ResultsToDataframe.KEY_TO_INDEX.keys()
    MAX_DIFF = 0.009

    def __init__(self, dataset_name, filename, df, mask_mode, check=True, with_gzip=False):
        assert(mask_mode in ["NM", "M"])

        self.df = PandasMethods.filename_df(df, filename, dataset_name)
        self.mask_mode = mask_mode
        self.data_columns_count = int((len(self.df.columns) - len(PandasUtils.FIXED_ROWS)) / 2)
        if check:
            PandasUtilsCheck(self, with_gzip).check_df(dataset_name)
        self.__calculate_percentage()

    #
    # For each data column 'column_x':
    # - Create a new column 'new_percentage_x' with the CR value
    # - Checks that |old column 'percentage_x' - new column 'new_percentage_x'| < MAX_DIFF
    # - Overwrites the old column 'percentage_x' with the values from new column 'new_percentage_x'
    #
    def __calculate_percentage(self):
        for value in range(1, self.data_columns_count + 1):  # [1, ... ]
            data_col_key = ResultsToDataframe.data_column_key(value)
            percentage_col_key = ResultsToDataframe.percentage_column_key(value)
            new_percentage_col_key = 'new_' + percentage_col_key

            base_coder_total = PandasMethods.coder_df(self.df, "CoderBase")[data_col_key].iloc[0]
            self.df[new_percentage_col_key] = 100 * (self.df[data_col_key] / base_coder_total)
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
        coder_df = PandasMethods.coder_df(self.df, coder_name)
        new_df = pd.DataFrame(columns=self.df.columns)
        for index, threshold in enumerate(ExperimentsUtils.THRESHOLDS):
            new_df.loc[index] = PandasMethods.get_min_row(coder_df, data_column_key, threshold).values
        return new_df

    def min_value_for_threshold(self, coder_name, column_index, threshold, nth=None):
        assert(threshold in ExperimentsUtils.THRESHOLDS)
        data_column_key = ResultsToDataframe.data_column_key(column_index)
        coder_df = PandasMethods.coder_df(self.df, coder_name) if coder_name is not None else self.df
        min_row = PandasMethods.get_min_row(coder_df, data_column_key, threshold, nth)
        return min_row

    def coder_base_df(self):
        return PandasMethods.coder_df(self.df, 'CoderBase').iloc[0]
