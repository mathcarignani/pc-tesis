import numpy as np
import pandas as pd

import sys
sys.path.append('.')

# import csv_converter.converter_utils as converter_utils
# from file_utils.csv_utils.csv_reader import CSVReader
# from parsers.parser_base import ParserBase


class PandasTools:
    # args = {
    #     'dataset': 'IRKIS',
    #     'no_data': 'N'
    # }
    def __init__(self, args):
        self.dataset = args['dataset']
        self.no_data = args['no_data']
        self.df = None

    def new_df(self, columns):
        self.df = pd.DataFrame(columns=columns)

    def add_row(self, timestamp, row):
        data = [np.nan if x == self.no_data else x for x in row]
        self.df.loc[timestamp] = data

    def print_stats(self):
        PandasTools.print_number("Total rows:", self.rows_count())
        PandasTools.print_number("Total nan rows:", self.nan_rows_count())

        columns = self.df.columns
        clean_df = self.df.dropna(axis=1, how='all')  # drop nan columns

        print "Total nan columns:", len(columns) - len(clean_df.columns)
        print "First timestamp:", clean_df.index[0]
        print "Last timestamp:", clean_df.index[-1]
        print "Min value:", clean_df.values.min()
        print "Max value:", clean_df.values.max()
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
        if self.dataset == 'IRKIS':
            self._plot_irkis(filename)
        elif self.dataset == 'NOAA':
            self._plot_noaa(filename)

    def _plot_irkis(self, filename):
        sensor_labels = ['A', 'B']
        for label in sensor_labels:
            label_columns = [col for col in self.df.columns if label in col]
            df_label = self.df[label_columns]  # remove columns from the other label
            title = 'Sensors with label ' + label + ' in ' + filename
            ax = df_label.plot(title=title, ylim=[0, 600])
            fig = ax.get_figure()
            fig.savefig(filename + '_' + label + '.png')

    def _plot_noaa(self, filename):
        pass
        # title = filename
        #
        # title = filename
        # df = self.df.copy(deep=True)
        # min_value = df.loc[df.idxmin()]['SST'][0]
        # max_value = df.loc[df.idxmax()]['SST'][0]
        # df['SSTnan'] = df['SST']
        # nan_value = min_value - (max_value - min_value) / 10
        # df['SSTnan'] = df['SSTnan'].apply(lambda x: nan_value if pd.isnull(x) else np.nan)
        #
        # fig, ax = plt.subplots()
        # df['SST'].plot(ax=ax, linestyle='none', title=title, marker='.', markersize=0.2)
        # df['SSTnan'].plot(ax=ax, linestyle='none', marker='.', markersize=1)
        # ax.legend()
        # fig = ax.get_figure()
        # fig.savefig(title + '.plot.png')
