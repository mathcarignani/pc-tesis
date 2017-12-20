import numpy as np
import pandas as pd

import sys
sys.path.append('.')

import csv_converter.converter_utils as converter_utils
from file_utils.csv_utils.csv_reader import CSVReader
from parsers.parser_base import ParserBase


class PandasTools:
    def __init__(self, input_path, input_filename):
        self.input_csv = CSVReader(input_path, input_filename)
        self.delta = None
        self.timestamp = None
        self.df = None
        self.column_length = 0

    def create_df(self):
        while self.df is None:
            row = self.input_csv.read_row()
            if row[0] == 'DELTA:':
                self.delta = converter_utils.parse_delta(row[1])
            elif row[0] == 'FIRST_TIMESTAMP:':
                self.timestamp = converter_utils.parse_datetime(row[1])
                print 'TTT'
                print row[1]
                print self.timestamp
            elif row[0] == 'Timestamp':
                self.df = pd.DataFrame(columns=row[2:])  # ignore "Missing"
                self.column_length = len(self.df.columns)

        while self.input_csv.continue_reading:
            row = self.input_csv.read_row()
            print row
            self.df.loc[self.timestamp] = self._parse_row(row)
            self.timestamp = converter_utils.timestamp_plus_delta(self.timestamp, self.delta)
        # self.df = self.df.set_index('Timestamp')

    def _parse_row(self, row):
        if row[1] == '1':  # Missing = '1'
            return np.array([np.nan] * len(self.df.columns))
        else:  # Missing = '0'
            data = [np.nan if x == ParserBase.NODATA else x for x in row[2:]]
            data = np.array(data).astype(np.float)
            return data

    def print_stats(self):
        self.print_number("Total rows:", self.rows_count())
        self.print_number("Total nan rows:", self.nan_rows_count())

        columns = self.df.columns
        clean_df = self.df.dropna(axis=1, how='all')  # drop nan columns

        print "Total nan columns:", len(columns) - len(clean_df.columns)
        print "First timestamp:", clean_df.index[0]
        print "Last timestamp:", clean_df.index[-1]
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

    def print_number(self, name, value):
        print name, "{0:,}".format(value)



# def plot(self, filename):
#     title = filename
#     df = self.df.copy(deep=True)
#     min_value = df.loc[df.idxmin()]['SST'][0]
#     max_value = df.loc[df.idxmax()]['SST'][0]
#     df['SSTnan'] = df['SST']
#     nan_value = min_value - (max_value - min_value) / 10
#     df['SSTnan'] = df['SSTnan'].apply(lambda x: nan_value if pd.isnull(x) else np.nan)
#
#     fig, ax = plt.subplots()
#     df['SST'].plot(ax=ax, linestyle='none', title=title, marker='.', markersize=0.2)
#     df['SSTnan'].plot(ax=ax, linestyle='none', marker='.', markersize=1)
#     ax.legend()
#     fig = ax.get_figure()
#     fig.savefig(title + '.plot.png')


