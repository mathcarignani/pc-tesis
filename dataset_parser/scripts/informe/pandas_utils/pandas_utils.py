import sys
sys.path.append('.')

import numpy as np
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.compress.experiments_utils import ExperimentsUtils


class PandasUtils(object):
    NUMBER_OF_COMBINATIONS = len(ExperimentsUtils.THRESHOLDS) * len(ExperimentsUtils.WINDOWS)
    FIXED_ROWS = ['coder', 'threshold', 'window']

    def __init__(self, dataset_name, df):
        self.dataset_name = dataset_name
        self.df = df
        self.data_columns_count = PandasUtils.__calculate_data_columns_count(df)
        self.__check_df()
        self.__calculate_percentage()

    def __check_df(self):
        coders = self.df['coder'].unique()
        np.testing.assert_array_equal(coders, ExperimentsUtils.CODERS)
        for coder in coders:
            rows, _ = self.df.loc[self.df['coder'] == coder].shape
            if coder == 'CoderBasic':
                assert(rows == 1)
            elif coder == 'CoderSF':
                assert(rows == len(ExperimentsUtils.THRESHOLDS))
            else:
                # the rest of the coders have the same number of rows
                assert(rows == self.NUMBER_OF_COMBINATIONS)

    @staticmethod
    def __calculate_data_columns_count(df):
        data_columns_count = (len(df.columns) - len(PandasUtils.FIXED_ROWS)) / 2
        assert()
        return data_columns_count

    def __calculate_percentage(self):
        pass

