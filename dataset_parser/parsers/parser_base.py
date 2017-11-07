import sys as sys


class ParserBase(object):
    def __init__(self):
        self.parsing_header = True
        self.nodata = None
        self.fail = {'missing_values': [], 'errors': [], 'duplicate_rows': []}
        self.last_date = None

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
