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

    def new_df(self, columns, extra_index=None):
        if extra_index:
            pipeinfo_index = pd.MultiIndex.from_tuples([tuple([None, None])], names=["Timestamp", extra_index])
            self.df = pd.DataFrame(index=pipeinfo_index, columns=columns)
            self.df.drop(np.nan, level='Timestamp', inplace=True)
        else:
            self.df = pd.DataFrame(columns=columns)

    def add_row(self, timestamp, row, extra_index=None):
        data = [np.nan if x == PandasTools.NO_DATA else x for x in row]
        if extra_index is None:
            if timestamp in self.df.index:
                self.logger.info("DUPLICATE TIMESTAMP")
                self.logger.info("timestamp = %s | data = %s", timestamp, data)
                self.logger.info("self.df.loc[timestamp]")
                self.logger.info("%s", self.df.loc[timestamp])
                # if not self.df.loc[timestamp].empty:
                #     raise StandardError()
                #     data = (data + self.df.loc[timestamp]) / 2
                #     self.logger.info("new_data = %s", data)
            self.df.loc[timestamp] = data
        else:  # extra_index is not None
            if (timestamp, extra_index) in self.df.index:
                self.logger.info("DUPLICATE INDEX")
            self.df.loc[(timestamp, extra_index), self.df.columns.values] = data # 1  #np.array([1,2,3], dtype='O') # np.array(data, dtype='O')

    def concat_df(self, new_df):
        if self.df is None:
            self.df = new_df
        else:
            self.df = pd.concat([self.df, new_df], axis=1)

    #
    # PRE: not(self.is_empty_df())
    #
    def df_to_csv(self, output_file):
        previous_timestamp = None
        if self.parser.NAME == 'ADCP':
            for index, row in self.df.iterrows():
                timestamp, depth = index
                values = [self.map_value(value) for value in row.values]
                if previous_timestamp is None:  # first row
                    timestamp_str = timestamp.strftime(converter_utils.DATE_FORMAT)
                else:
                    delta = timestamp - previous_timestamp  # >= 0
                    timestamp_str = converter_utils.format_timedelta(delta)
                output_file.write_row([timestamp_str, depth] + values)
                previous_timestamp = timestamp
        else:
            for timestamp, row in self.df.iterrows():
                values = [self.map_value(value) for value in row.values]
                if previous_timestamp is None:  # first row
                    timestamp_str = timestamp.strftime(converter_utils.DATE_FORMAT)
                else:
                    delta = timestamp - previous_timestamp  # always positive
                    timestamp_str = converter_utils.format_timedelta(delta)
                output_file.write_row([timestamp_str] + values)
                previous_timestamp = timestamp

    @classmethod
    def map_value(cls, value):
        # OTHER
        # return cls.NO_DATA if pd.isnull(value) else round(float(value)*1000, 0)
        # NOAA
        return cls.NO_DATA if pd.isnull(value) else round(float(value)*1000, 0)

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
        first_timestamp, last_timestamp = clean_df.index[0], clean_df.index[-1]
        self.logger.info("First timestamp: %s", first_timestamp)
        self.logger.info("Last timestamp: %s", last_timestamp)
        diff_s = (last_timestamp - first_timestamp).total_seconds()
        diff_m, diff_h, diff_d = divmod(diff_s, 60)[0], divmod(diff_s, 3600)[0], divmod(diff_s, 86400)[0]
        self.logger.info("Last timestamp - First timestamp: %s sec | %s min | %s hours | %s days",
                     diff_s, diff_m, diff_h, diff_d)
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
