import numpy as np
import pandas as pd
import sys
sys.path.append('.')

import csv_converter.converter_utils as converter_utils


class PandasTools:
    NO_DATA = "N"

    def __init__(self, parser, logger):
        self.parser = parser
        self.logger = logger
        self.df = None
        self.empty_df = None
        # initialized in new_df
        self.repeat_timestamp = None

    #
    # repeat_timestamp is True if it is expected that the same timestamp can be repeated
    #
    def new_df(self, columns, repeat_timestamp):
        cols = columns if not repeat_timestamp else ['Timestamp'] + columns
        self.df = pd.DataFrame(columns=cols)
        self.repeat_timestamp = repeat_timestamp

    def add_row(self, timestamp, row, adcp=False):
        print timestamp
        data = [np.nan if x == PandasTools.NO_DATA else x for x in row]
        if adcp:
            # row = [depth, UCUR, VCUR, WCUR]
            depth = row[0]
            for idx, component in enumerate(['UCUR', 'VCUR', 'WCUR']):
                col = adcp + "_" + str(int(depth)) + "_" + component
                self.df.loc[timestamp, col] = row[1 + idx]
        elif self.repeat_timestamp:
            self.df.loc[len(self.df)] = [timestamp] + data
        else:
            self.df.loc[timestamp] = data

    def concat_df(self, new_df):
        if self.df is None:
            self.df = new_df
        else:
            # print "self.df", self.df
            # print "self.df.shape", self.df.shape
            self.df = pd.concat([self.df, new_df], axis=1)
            # print "self.df", self.df
            # print "self.df.shape", self.df.shape

    #
    # PRE:
    # (1) not(self.is_empty_df())
    # (2) time_unit in ['minutes']
    #
    def df_to_csv(self, output_file, time_unit):
        previous_timestamp = self._first_timestamp()
        # if self.parser.NAME == 'ADCP':
        #     for index, row in self.df.iterrows():
        #         timestamp, depth = index
        #         values = [self.map_value(value) for value in row.values]
        #         if previous_timestamp is None:  # first row
        #             timestamp_str = timestamp.strftime(converter_utils.DATE_FORMAT)
        #         else:
        #             delta = timestamp - previous_timestamp  # >= 0
        #             timestamp_str = converter_utils.format_timedelta(delta)
        #         output_file.write_row([timestamp_str, depth] + values)
        #         previous_timestamp = timestamp
        # else:
        for timestamp, row in self.df.iterrows():
            if self.repeat_timestamp:
                timestamp = row[0]
                row = row[1:]
            values = [self.map_value(value) for value in row.values]
            delta = timestamp - previous_timestamp  # always positive
            timestamp_str = converter_utils.format_timedelta(delta, time_unit)
            output_file.write_row([timestamp_str] + values)
            previous_timestamp = timestamp

    def _first_timestamp(self):
        return self.df['Timestamp'].iloc[0] if self.repeat_timestamp else self.df.index.min()

    def first_timestamp(self):
        timestamp_str = self._first_timestamp().strftime(converter_utils.DATE_FORMAT)
        return timestamp_str

    @classmethod
    def map_value(cls, value):
        return cls.NO_DATA if pd.isnull(value) else int(value)

    def print_stats(self):
        total_rows, nan_rows = self.rows_count(), self.nan_rows_count()
        self.empty_df = total_rows == nan_rows
        self.print_number("Total rows:", total_rows)
        self.print_number("Total nan rows:", nan_rows)

        if total_rows > nan_rows:
            columns = self.df.columns
            clean_df = self.df.dropna(axis=1, how='all')  # drop nan columns

            self.logger.info("Total nan columns: %s", len(columns) - len(clean_df.columns))
            if self.parser.asc_timestamp:
                self._asc_timestamp_stats(clean_df)
            self.logger.info("\nDataset stats:")
            self.logger.info(clean_df.describe(include='all', percentiles=[]))
            self.logger.info("")
            self.logger.info("Null values count for each column:")
            self.logger.info(clean_df.isnull().sum())
        self.logger.info("")

    #
    # These stats only make sense for datasets in which the timestamp is always ASC
    #
    def _asc_timestamp_stats(self, clean_df):
        if self.repeat_timestamp:
            first_timestamp, last_timestamp = clean_df['Timestamp'].iloc[0], clean_df['Timestamp'].iloc[-1]
        else:
            first_timestamp, last_timestamp = clean_df.index[0], clean_df.index[-1]
        self.logger.info("First timestamp: %s", first_timestamp)
        self.logger.info("Last timestamp: %s", last_timestamp)
        diff_s = (last_timestamp - first_timestamp).total_seconds()
        diff_m, diff_h, diff_d = divmod(diff_s, 60)[0], divmod(diff_s, 3600)[0], divmod(diff_s, 86400)[0]
        self.logger.info("Last timestamp - First timestamp: %s sec | %s min | %s hours | %s days",
                     diff_s, diff_m, diff_h, diff_d)
        if not self.repeat_timestamp:
            self.logger.info("Min value: %s", np.nanmin(clean_df.values))
            self.logger.info("Max value: %s", np.nanmax(clean_df.values))

    def rows_count(self):
        return len(self.df.index)

    def nan_rows_count(self):
        return len(self.df.index[self.df.isnull().all(1)])

    def is_empty_df(self):
        if self.empty_df is None:
            total_rows, nan_rows = self.rows_count(), self.nan_rows_count()
            self.empty_df = total_rows == nan_rows
        return self.empty_df

    def print_number(self, name, value):
        self.logger.info("%s %s", name, "{0:,}".format(value))
