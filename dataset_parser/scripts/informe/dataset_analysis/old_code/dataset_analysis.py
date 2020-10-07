import sys
sys.path.append('.')

import pandas as pd
from scripts.informe.data_analysis.process_results.process_results import ProcessResults
from scripts.compress.experiments_utils import ExperimentsUtils
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools


class DatasetAnalysis(object):
    @staticmethod
    def append_df(dataset_name, filename, col_index, col_name, column_df):
        filename_path = ExperimentsUtils.get_dataset_path(dataset_name) + "/" + filename
        file_df = pd.read_csv(filename_path, skiprows=3, na_values=PandasTools.NO_DATA)
        file_df.drop(['Time Delta'], axis=1, inplace=True)  # remove Time Delta column

        new_col_df = pd.DataFrame(columns=[col_name])
        columns_count = ExperimentsUtils.get_dataset_data_columns_count(dataset_name)
        for i, column in enumerate(file_df.columns):
            if i % columns_count == (col_index - 1):
                col_df = pd.DataFrame(columns=[col_name])
                col_df[col_name] = file_df[column]
                # print str(i) + " => " + str(col_df.shape)
                new_col_df = new_col_df.append(col_df, ignore_index=True)

        # print new_col_df.shape

        if column_df is None:
            return new_col_df
        else:
            column_df = column_df.append(new_col_df, ignore_index=True)
            return column_df

    @staticmethod
    def print_df_analysis(df, csv_writer):
        rows, cols = df.shape
        assert(cols == 1)

        column_name = df.columns.values[0]

        mz_table = DatasetAnalysis.missing_zero_values_table(df)
        nan_total = mz_table['Missing Values'].values[0]
        nan_perc = mz_table['% of Total Values'].values[0]

        # print df.describe()
        min_, max_ = int(df.min().values[0]), int(df.max().values[0])
        if max_ > 0:
            range_ = max_ - min_ + 1
        else:
            range_ = -(min_ + max_) + 1
        mean, std = df.mean().values[0], df.std().values[0]

        rows = '{:,}'.format(rows)
        nan_total = '{:,}'.format(nan_total)
        min_ = '{:,}'.format(min_)
        max_ = '{:,}'.format(max_)
        range_ = '{:,}'.format(range_)

        nan_perc = str(round(nan_perc, 2))
        mean = '{:,}'.format(round(mean, 2))
        std = '{:,}'.format(round(std, 2))

        csv_writer.write_row([None, column_name, rows, None, nan_total, nan_perc, None, min_, max_, range_, None, mean, std])

    #
    # SOURCE: https://stackoverflow.com/a/55455380/4547232
    #
    @staticmethod
    def missing_zero_values_table(df):
        zero_val = (df == 0.00).astype(int).sum(axis=0)
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mz_table = pd.concat([zero_val, mis_val, mis_val_percent], axis=1)
        mz_table = mz_table.rename(
        columns = {0 : 'Zero Values', 1 : 'Missing Values', 2 : '% of Total Values'})
        mz_table['Total Zero Missing Values'] = mz_table['Zero Values'] + mz_table['Missing Values']
        mz_table['% Total Zero Missing Values'] = 100 * mz_table['Total Zero Missing Values'] / len(df)
        mz_table['Data Type'] = df.dtypes
        # mz_table = mz_table[
        #     mz_table.iloc[:,1] != 0].sort_values(
        # '% of Total Values', ascending=False).round(1)
        # print ("Your selected dataframe has " + str(df.shape[1]) + " columns and " + str(df.shape[0]) + " Rows.\n"
        #     "There are " + str(mz_table.shape[0]) +
        #       " columns that have missing values.")
        return mz_table


class DatasetAnalysisScript(object):
    OUT_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/dataset_analysis/out"
    COLUMNS = ["Dataset", "Column", "#Rows", None, "#N", "#N (%)", None, "Min", "Max", "Range", None, "Mean", "STD"]

    def __init__(self):
        self.debug_mode = True
        self.csv_writer = CSVWriter(self.OUT_PATH, 'output.csv')

    def run(self):
        self.csv_writer.write_row(self.COLUMNS)
        self.__datasets_iteration()

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            self._print(self.dataset_name)
            self.csv_writer.write_row([ExperimentsUtils.get_dataset_short_name(self.dataset_name)])
            self.__columns_iteration()

    def __columns_iteration(self):
        dataset_filenames = ProcessResults.dataset_filenames(self.dataset_name, False)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self._print(self.col_name, 1)
            self.column_dataframe = None
            self.__filenames_iteration(dataset_filenames)

    def __filenames_iteration(self, dataset_filenames):
        column_df = None
        for self.filename in dataset_filenames:
            self._print(self.filename, 2)
            column_df = DatasetAnalysis.append_df(self.dataset_name, self.filename, self.col_index, self.col_name, column_df)
        print column_df.shape
        DatasetAnalysis.print_df_analysis(column_df, self.csv_writer)

    def _print(self, value, spaces=0):
        if self.debug_mode:
            print " " * (spaces * 2) + value

DatasetAnalysisScript().run()
