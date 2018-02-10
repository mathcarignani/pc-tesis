import numpy as np
import pandas as pd

import sys
sys.path.append('.')

# import csv_converter.converter_utils as converter_utils
# from file_utils.csv_utils.csv_reader import CSVReader
# from parsers.parser_base import ParserBase


class PandasTools:
    NO_DATA = "N"

    def __init__(self, dataset_utils):
        self.dataset_utils = dataset_utils
        self.df = None

    def new_df(self, columns):
        self.df = pd.DataFrame(columns=columns)

    def add_row(self, timestamp, row):
        data = [np.nan if x == PandasTools.NO_DATA else x for x in row]
        self.df.loc[timestamp] = data

    def print_stats(self):
        PandasTools.print_number("Total rows:", self.rows_count())
        PandasTools.print_number("Total nan rows:", self.nan_rows_count())

        columns = self.df.columns
        clean_df = self.df.dropna(axis=1, how='all')  # drop nan columns

        print "Total nan columns:", len(columns) - len(clean_df.columns)
        print "First timestamp:", clean_df.index[0]
        print "Last timestamp:", clean_df.index[-1]
        print "Min value:", np.nanmin(clean_df.values)
        print "Max value:", np.nanmax(clean_df.values)
        print
        print "Dataset stats:"
        print clean_df.describe(percentiles=[])
        print
        print "Null values count for each column:"
        print clean_df.isnull().sum()
        print

    def rows_count(self):
        return len(self.df.index)

    def nan_rows_count(self):
        return len(self.df.index[self.df.isnull().all(1)])

    @staticmethod
    def print_number(name, value):
        print name, "{0:,}".format(value)

    def plot(self, filename):
        self.dataset_utils.plot(filename, self.df)
