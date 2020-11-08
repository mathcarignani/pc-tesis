import sys
sys.path.append('.')

import pandas as pd
from pandas_tools.pandas_tools import PandasTools


class PandasAnalysis(object):
    @staticmethod
    def get_data(file_path, columns_length=None):
        print(file_path)
        df = PandasAnalysis.load_df(file_path)
        if columns_length is None:
            return PandasAnalysis.get_data_object(df)
        else:
            return PandasAnalysis.get_data_array(df, columns_length)

    @staticmethod
    def get_data_array(df, columns_length):
        print(df)
        total_columns = len(df.columns)
        assert(total_columns % columns_length == 0)

        data_array = []
        for col_index in range(0, columns_length):
            new_df = df.copy(deep=False)
            name = new_df.columns.tolist()[col_index] # 1_AirTemp
            common_name = name[2:len(name)] # AirTemp
            print(name)
            print(common_name)
            new_df = new_df.filter(like=common_name)
            assert(len(new_df.columns) == total_columns / columns_length)
            data = PandasAnalysis.get_data_object(new_df)
            data_array.append(data)
        return data_array

    @staticmethod
    def get_data_object(df):
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

    @staticmethod
    def load_df(file_path):
        df = pd.read_csv(file_path, skiprows=3, na_values=PandasTools.NO_DATA)
        df.drop(['Time Delta'], axis=1, inplace=True)  # remove Time Delta column
        return df
