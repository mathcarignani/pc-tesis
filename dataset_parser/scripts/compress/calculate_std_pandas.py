import sys
sys.path.append('.')

import pandas as pd
import numpy as np
from pandas_tools.pandas_tools import PandasTools


class CalculateSTDPandas:
    def __init__(self, input_path, input_filename):
        filename_path = input_path + "/" + input_filename
        self.df = pd.read_csv(filename_path, skiprows=3, na_values=PandasTools.NO_DATA)

    def calculate_stds(self):
        #
        # About STDEVP:
        # https://stackoverflow.com/a/14894143/4547232
        # https://stackoverflow.com/a/52642277/4547232
        #
        df_stds = self.df.std(ddof=0)
        stds = list(df_stds)
        stds = [PandasTools.NO_DATA if np.isnan(value) else value for value in stds]
        return stds
