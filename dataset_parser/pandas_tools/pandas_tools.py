import logging
import numpy as np
import pandas as pd

import sys
sys.path.append('.')


class PandasTools:
    NO_DATA = "N"

    def __init__(self, parser):
        self.df = None
        self.parser = parser

    def new_df(self, columns):
        self.df = pd.DataFrame(columns=columns)

    def add_row(self, timestamp, row):
        data = [np.nan if x == PandasTools.NO_DATA else x for x in row]
        self.df.loc[timestamp] = data

    def print_stats(self):
        total_rows, nan_rows = self.rows_count(), self.nan_rows_count()
        PandasTools.print_number("Total rows:", total_rows)
        PandasTools.print_number("Total nan rows:", nan_rows)

        if total_rows > nan_rows:
            columns = self.df.columns
            clean_df = self.df.dropna(axis=1, how='all')  # drop nan columns

            logging.info("Total nan columns: %s", len(columns) - len(clean_df.columns))
            if self.parser.asc_timestamp:
                self._asc_timestamp_stats(clean_df)
            logging.info("\nDataset stats:")
            logging.info(clean_df.describe(include='all', percentiles=[]))
            logging.info("")
            logging.info("Null values count for each column:")
            logging.info(clean_df.isnull().sum())
        logging.info("")

    #
    # These stats only make sense for datasets in which the timestamp is always ASC
    #
    def _asc_timestamp_stats(self, clean_df):
        first_timestamp, last_timestamp = clean_df.index[0], clean_df.index[-1]
        logging.info("First timestamp: %s", first_timestamp)
        logging.info("Last timestamp: %s", last_timestamp)
        diff_s = (last_timestamp - first_timestamp).total_seconds()
        diff_m, diff_h, diff_d = divmod(diff_s, 60)[0], divmod(diff_s, 3600)[0], divmod(diff_s, 86400)[0]
        logging.info("Last timestamp - First timestamp: %s sec | %s min | %s hours | %s days",
                     diff_s, diff_m, diff_h, diff_d)
        logging.info("Min value: %s", np.nanmin(clean_df.values))
        logging.info("Max value: %s", np.nanmax(clean_df.values))

    def rows_count(self):
        return len(self.df.index)

    def nan_rows_count(self):
        return len(self.df.index[self.df.isnull().all(1)])

    @staticmethod
    def print_number(name, value):
        logging.info("%s %s", name, "{0:,}".format(value))
