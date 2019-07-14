import sys
sys.path.append('.')

from scripts.informe.plot.plot_constants import PlotConstants
from scripts.compress.compress_aux import ExperimentsConstants

class PandasUtils(object):
    def __init__(self, df):
        self.df = df
        self.__check_df()

    def __check_df(self):
        # the rest of the coders have the same number of rows
        number_of_combinations = len(ExperimentsConstants.THRESHOLDS) * len(ExperimentsConstants.WINDOWS)
        coders = self.df['coder'].unique()
        assert(coders == ExperimentsConstants.CODERS)
        for coder in coders:
            rows, _ = self.df.loc[self.df['coder'] == coder].shape
            if coder == 'CoderBasic':
                assert(rows == 1)
            elif coder == 'CoderSF':
                assert(rows == len(ExperimentsConstants.THRESHOLDS))
            else:
                assert(rows == number_of_combinations)
