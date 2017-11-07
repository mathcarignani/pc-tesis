import numpy as np
import pandas as pd
import sys as sys


class Parser(object):
    def __init__(self):
        self.parsing_header = True
        self.fail = {'missing_values': [], 'errors': [], 'duplicate_rows': []}
        self.last_date = None
        self.nodata = None

    def parse_line(self, line):
        if self.parsing_header:
            self.parsing_header = self._parse_header(line)
            if not (self.parsing_header) and not (self.nodata):
                raise StandardError('The nodata attribute is missing.')
        else:
            self._parse_data(line)

    def _parse_header(self, line):
        raise NotImplementedError("This method must be implemented.")

    def _parse_columns(self, s_line):
        # EXAMPLE:
        # fields       = timestamp TA TSS TSG VW DW VW_MAX ISWR OSWR ILWR PSUM HS RH
        # self.df = pd.DataFrame(columns=s_line[1:])
        # self.columns_count = len(self.df.columns)

        # YYYYMMDD HHMMSS    SST Q M
        self.df = pd.DataFrame(columns=[s_line[2]])
        self.columns_count = len(self.df.columns)

    def _parse_data(self, line):
        # EXAMPLE:
        # 2009-10-01T01:00  279.26   275.43   275.43    1.1     0    0.0      0      0 271.947  0.000    0.000   1.000
        # s_line = line.split()
        # try:
        # 	np_array = None
        # 	current_date = s_line[0]
        # 	timestamp = pd.to_datetime(current_date)
        # 	data = s_line[1:]
        # 	if len(data) == self.columns_count:
        # 		if current_date == self.last_date:
        # 			self.fail['duplicate_rows'].append(line)
        # 		else:
        # 			data = [np.nan if x == self.nodata else x for x in data]
        # 			np_array = np.array(data).astype(np.float)
        # 			self.last_date = current_date
        # 	else:
        # 		# if the line has an inconsistent number of values mark the whole row as invalid
        # 		self.fail['missing_values'].append(line)
        # 		np_array = np.array([np.nan] * len(self.df.columns))

        # 	if np_array is not None:
        # 		self.df.loc[timestamp] = np_array

        # except:
        # 	self.fail['errors'].append(line)

        # 20170101 000000 22.940 2 R
        s_line = line.split()

        try:
            date = s_line[0] + ' ' + s_line[1]
            timestamp = pd.to_datetime(date, format='%Y%m%d %H%M%S')
            data = np.array([s_line[2]])
            # print data
            data = [np.nan if x == self.nodata else x for x in data]
            np_array = np.array(data).astype(np.float)
            # print timestamp
            # print np_array
            self.df.loc[timestamp] = np_array

        except:
            self.fail['errors'].append(line)

    def process_data(self):
        print "Total dataset length:", len(self.df.index)
        print "Total nan rows:", len(self.df.index[self.df.isnull().all(1)])
        # drop nan columns
        columns = self.df.columns
        self.df = self.df.dropna(axis=1, how='all')
        print "Total nan columns:", len(columns) - len(self.df.columns)
        print "First timestamp:", self.df.index[0]
        print "Last timestamp:", self.df.index[-1]
        print "Dataset stats:"
        print self.df.describe(percentiles=[])
        print
        print "Null values count for each column:"
        print self.df.isnull().sum()
        print
        print "Invalid lines (duplicate rows) -", len(self.fail['duplicate_rows'])
        for p in self.fail['duplicate_rows']: sys.stdout.write(p)
        print
        print "Invalid lines (missing values) -", len(self.fail['missing_values'])
        for p in self.fail['missing_values']: sys.stdout.write(p)
        print
        print "Invalid lines (errors) -", len(self.fail['errors'])
        for p in self.fail['errors']: sys.stdout.write(p)
