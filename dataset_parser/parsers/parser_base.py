from utils import Utils
import sys as sys
import numpy as np


class ParserBase(object):
    def __init__(self):
        self.parsing_header = True
        self.nodata = None
        self.errors = {'missing_values': [], 'errors': [], 'duplicate_rows': []}
        self.last_date = None  # used to catch duplicate dates

    def parse_line(self, line):
        if self.parsing_header:
            self.parsing_header = self._parse_header(line)
            if not self.parsing_header and not self.nodata:
                raise StandardError('Finished parsing header and nodata value is unknown.')
        else:
            self._parse_data(line)

    def _parse_header(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _parse_columns(self, s_line):
        raise NotImplementedError("This method must be implemented.")

    def _parse_data(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _clean_data(self, data):
        data = [np.nan if x == self.nodata else x for x in data]
        data = np.array(data).astype(np.float)
        return data

    def process_data(self):
        Utils.print_number("Total rows:", self.rows_count())
        Utils.print_number("Total nan rows:", self.nan_rows_count())

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
        for key in self.errors.keys():
            print "Invalid lines -", key, "-", len(self.errors[key])
            for p in self.errors[key]: sys.stdout.write(p)
            print

    def rows_count(self):
        return len(self.df.index)

    def nan_rows_count(self):
        return len(self.df.index[self.df.isnull().all(1)])
