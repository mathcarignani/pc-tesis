import sys
sys.path.append('.')

import pandas as pd
from pandas_tools.pandas_tools import PandasTools


class PandasAnalysis(object):

    @staticmethod
    def get_data(file_path):
        df = pd.read_csv(file_path, skiprows=3, na_values=PandasTools.NO_DATA)
        df.drop(['Time Delta'], axis=1, inplace=True)  # remove Time Delta column

        rows, cols = df.shape
        total = rows*cols

        df_stack = df.stack()

        minimum = df_stack.min()
        assert(minimum == df.min().min())

        maximum = df_stack.max()
        assert(maximum == df.max().max())

        mean = df_stack.mean()
        median = df_stack.median()
        std = df_stack.std()
        nan_total = df.isnull().sum(axis = 0).sum()
        nan_percentage = (100.0 / total) * nan_total

        print(df.describe())
        print(df.isnull().sum(axis = 0)) # total nan values in each column
        print(nan_total)

        data = {
            'rows': rows, 'columns': cols, 'total_entries': total,
            'nan_total': nan_total, 'nan_percentage': nan_percentage,
            'min': minimum, 'max': maximum,
            'mean': mean, 'median': median, 'stdev': std,

        }
        return data
