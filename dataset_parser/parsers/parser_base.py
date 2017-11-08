from utils import Utils
import sys as sys
import numpy as np


class ParserBase(object):
    def __init__(self):
        self.parsing_header = True
        self.nodata = None
        self.fail = {'missing_values': [], 'errors': [], 'duplicate_rows': []}
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
        self.df = self.df.dropna(axis=1, how='all')  # drop nan columns

        print "Total nan columns:", len(columns) - len(self.df.columns)
        print "First timestamp:", self.df.index[0]
        print "Last timestamp:", self.df.index[-1]
        print "Dataset stats:"
        print self.df.describe(percentiles=[])
        print
        print "Null values count for each column:"
        print self.df.isnull().sum()
        print
        for key in self.fail.keys():
            print "Invalid lines -", key, "-", len(self.fail[key])
            for p in self.fail[key]: sys.stdout.write(p)
            print

    def rows_count(self):
        return len(self.df.index)

    def nan_rows_count(self):
        return len(self.df.index[self.df.isnull().all(1)])
