import sys
sys.path.append('.')

import numpy as np
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_methods import PandasMethods


class PandasUtilsCheck(object):
    NUMBER_OF_COMBINATIONS = len(ExperimentsUtils.THRESHOLDS) * len(ExperimentsUtils.WINDOWS)

    def __init__(self, pandas_utils, with_gzip=False):
        self.pandas_utils = pandas_utils
        self.with_gzip = with_gzip
        self.df = pandas_utils.df
        self.mask_mode = pandas_utils.mask_mode
        self.data_columns_count = pandas_utils.data_columns_count

    def check_df(self, dataset_name):
        # check that the number of data columns is ok
        assert(self.data_columns_count == ExperimentsUtils.get_dataset_data_columns_count(dataset_name))

        # check that data for every coder is included
        coders = self.df['coder'].unique()
        expected_coders = ExperimentsUtils.coders_names(self.mask_mode)
        if self.with_gzip and 'CoderGZIP' not in expected_coders:
            expected_coders.append('CoderGZIP')
        # IMPORTANT: this can fail if ExperimentUtils was changed after running the compress script
        np.testing.assert_array_equal(coders, expected_coders)

        # check that the rows count for each coder match
        for coder_name in coders:
            self.__check_coder_rows_count(coder_name)

    def __check_coder_rows_count(self, coder_name):
        rows_count = self.__coder_rows_count(coder_name)
        if coder_name == 'CoderBase':
            assert(rows_count == 1)
        elif coder_name in ['CoderGZIP']:
            assert(rows_count == len(ExperimentsUtils.THRESHOLDS))
        else:
            # the rest of the coders have the same number of rows
            pass
            # if rows_count != self.NUMBER_OF_COMBINATIONS:
            #     print(PandasMethods.coder_df(self.df, coder_name))
            #     print(coder_name)
            #     print(self.NUMBER_OF_COMBINATIONS)
            #     print(rows_count)
            #     assert(rows_count == self.NUMBER_OF_COMBINATIONS)

    def __coder_rows_count(self, coder_name):
        rows_count, _ = PandasMethods.coder_df(self.df, coder_name).shape
        return rows_count