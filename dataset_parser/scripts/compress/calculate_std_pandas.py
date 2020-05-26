import sys
sys.path.append('.')

import pandas as pd
import numpy as np
from pandas_tools.pandas_tools import PandasTools
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.compress.calculate_std_manual import CalculateSTDManual


class CalculateSTDPandas:
    COMPARE = True

    def __init__(self, input_path, input_filename):
        self.input_path = input_path
        self.input_filename = input_filename
        self.filename_path = input_path + "/" + input_filename

    def calculate_stds(self):
        stds = self._calculate_stds_pandas()
        if self.COMPARE:
            self.compare_with_manual_std(stds)
        return stds

    #
    # Compare the stds obtained by pandas against the stds calculated manually.
    #
    def compare_with_manual_std(self, stds):
        manual_stds = CalculateSTDManual.calculate_stds(self.input_path, self.input_filename)

        assert(len(stds) == len(manual_stds))

        diff = []
        for index in range(len(stds)):
            value, value_manual  = stds[index], manual_stds[index]

            if value == PandasTools.NO_DATA:
                assert(value == value_manual)  # both values must be equal to PandasTools.NO_DATA
                diff.append(value)
            else:
                diff.append(value - value_manual)

        minimum = min([10 if value == PandasTools.NO_DATA else value for value in diff])
        assert(abs(minimum) < pow(10, -10))


    def _calculate_stds_pandas(self):
        df = pd.read_csv(self.filename_path, skiprows=3, na_values=PandasTools.NO_DATA)  # skip first 3 rows (header)
        #
        # About STDEVP:
        # https://stackoverflow.com/a/14894143/4547232
        # https://stackoverflow.com/a/52642277/4547232
        #
        df_stds = df.std(ddof=0)
        stds = list(df_stds)
        stds = [PandasTools.NO_DATA if np.isnan(value) else value for value in stds]
        return stds


    @classmethod
    def calculate_error_thresholds(cls, stds, param_e_list=ExperimentsUtils.THRESHOLDS):
        percentages = [param / 100 for param in param_e_list] # [0.0, 0.01, 0.03, 0.05, 0.1, 0.15, 0.2, 0.3]

        res = []
        for percentage in percentages:
            stds[0] = 0  # the error threshold for the timedelta is always 0

            values = []
            for std in stds:
                if std == PandasTools.NO_DATA:
                    values.append(PandasTools.NO_DATA)
                else:
                    value = int(round(std * percentage, 0))
                    values.append(value)
            res.append({'percentage': percentage, 'values': values})
        return res