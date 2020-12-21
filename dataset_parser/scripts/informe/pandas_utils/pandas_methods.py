import sys
sys.path.append('.')

import pandas as pd
from auxi.python_utils import assert_equal_lists


class PandasMethods(object):
    #
    # Given a df, it filters the rows which belong to a filename (and a dataset if given)
    #
    @staticmethod
    def filename_df(df, filename, dataset):
        df = df.loc[df['filename'] == filename]
        df = PandasMethods.dataset_df(df, dataset)
        df = df.dropna(axis=1, how='all')  # drop the columns where all elements are NaN
        return df

    #
    # Deep copy df
    #
    @staticmethod
    def copy(df):
        return pd.DataFrame.copy(df, deep=True)

    #
    # Given a df, it filters the rows which belong to a certain dataset
    #
    @staticmethod
    def dataset_df(df, dataset):
        return df.loc[df['dataset'] == dataset]

    #
    # Given a df, it filters the rows which belong to a certain coder
    #
    @staticmethod
    def coder_df(df, coder_name):
        return df.loc[df['coder'] == coder_name]

    #
    # Given a df, it filters the rows which belong to a certain threshold
    #
    @staticmethod
    def threshold_df(df, threshold):
        return df.loc[df['threshold'] == threshold]

    #
    # Given a coder_df, a column_key, and a threshold:
    # it returns the row with the (nth) minimum value for that column for that <coder, threshold> combination
    #
    @staticmethod
    def get_min_row(coder_df, column_key, threshold, nth=None):
        coder_name = coder_df.coder.values[0]
        dataset = coder_df.dataset.values[0]
        if len(coder_df) == 1:  # and coder_df.loc[0].coder == 'CoderBase':
            assert(coder_df.coder.values[0] == 'CoderBase')
            min_value_index = coder_df.index.values[0]
            min_value_row = coder_df.loc[min_value_index]
            return min_value_row

        thresholds = coder_df.threshold.unique()
        check_same = set([0, 1, 3, 5, 10, 15, 20, 30]).issubset(set(thresholds))
        if not check_same:
            print(thresholds)
            assert(check_same)
        threshold_df = PandasMethods.threshold_df(coder_df, threshold)

        min_value_index = threshold_df[column_key].idxmin()
        min_value_row = threshold_df.loc[min_value_index]

        if nth:
            # nth_min_values_df = threshold_df[column_key].nsmallest(nth)
            # nth_min_value_index = nth_min_values_df.index[nth-1]
            # min_value_index = nth_min_value_index
            # min_value_row = threshold_df.loc[min_value_index]
            best_coder = min_value_row.coder
            threshold_df = threshold_df[threshold_df.coder != best_coder]
            min_value_index = threshold_df[column_key].idxmin()
            min_value_row = threshold_df.loc[min_value_index]

        min_value = min_value_row[column_key]
        min_value_rows_count = threshold_df[threshold_df[column_key] == min_value].count()[column_key]

        # cases in which for a single combination there are two combinations with minimum CR
        if coder_name == "CoderGAMPSLimit" and column_key == "column_2" and threshold == 30 and dataset == "NOAA-SPC-tornado":
            assert(min_value_rows_count == 2)
        elif coder_name == "CoderSF" and column_key == "column_1" and threshold == 0 and dataset == "NOAA-SPC-hail":
            assert(min_value_rows_count == 2)
        elif coder_name == "CoderSF" and column_key == "column_2" and threshold == 0 and dataset == "NOAA-SPC-hail":
            assert(min_value_rows_count == 4)
        elif coder_name == "CoderSF" and column_key == "column_2" and threshold == 0 and dataset == "NOAA-SPC-tornado":
            assert(min_value_rows_count == 2)
        else:
            # print(coder_name)
            # print(column_key)
            # print(threshold)
            # print(dataset)
            assert(min_value_rows_count == 1)
        return min_value_row

    #
    # Given a df, it returns a list with the names of every column
    #
    @staticmethod
    def column_names(df):
        return df.columns.values

    #
    # Given a df, it returns a list with the names of every data column
    @staticmethod
    def data_column_names(df):
        return [col for col in PandasMethods.column_names(df) if 'column' in col]

    #
    # Given a df, it returns a list with every dataset
    #
    @staticmethod
    def datasets(df):
        return df['dataset'].unique()

    #
    #
    # Given a df, it returns a list with every filename
    #
    @staticmethod
    def filenames(df, dataset=None):
        if dataset:
            df = PandasMethods.dataset_df(df, dataset)
        return df['filename'].unique()

    #
    # Check that for every file the CoderBase values match for every column
    #
    @staticmethod
    def check_coder_base_matches(df0, df3):
        base_df_NM = PandasMethods.coder_df(df0, 'CoderBase')
        base_df_M = PandasMethods.coder_df(df3, 'CoderBase')

        datasets_df_NM = PandasMethods.datasets(base_df_NM)
        datasets_df_M = PandasMethods.datasets(base_df_M)
        assert_equal_lists(datasets_df_NM, datasets_df_M)

        for dataset in datasets_df_NM:
            filenames_df_NM = PandasMethods.filenames(base_df_NM, dataset)
            filenames_df_M = PandasMethods.filenames(base_df_M, dataset)
            assert_equal_lists(filenames_df_NM, filenames_df_M)

            for filename in filenames_df_NM:
                filename_rows_0 = PandasMethods.filename_df(base_df_NM, filename, dataset)
                filename_rows_3 = PandasMethods.filename_df(base_df_M, filename, dataset)
                assert(len(filename_rows_0.index) == 1 and len(filename_rows_3.index) == 1)

                column_names_0 = PandasMethods.data_column_names(filename_rows_0)
                column_names_3 = PandasMethods.data_column_names(filename_rows_3)
                assert_equal_lists(column_names_0, column_names_3)

                for col in column_names_0:
                    rows0, rows3 = filename_rows_0[col], filename_rows_3[col]
                    assert(len(rows0) == 1)
                    assert(len(rows3) == 1)
                    value0, value3 = rows0.iloc[0], rows3.iloc[0]
                    assert(value0 == value3)
