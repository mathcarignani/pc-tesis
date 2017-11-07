from parser import *


# Platform: T0N95W 2017-01-01 to 2017-11-03 (31142 total rows, 2 deployments) File Generated on 2017-11-05
# Parameter(s): Sea Surface Temperature ("degree celsius"), -9.999 = missing
# Deployment: DM179A-20160312 2017-01-01 to 2017-03-27 (11995 data rows, 1 depth columns)
# Depth (Meters)       1 Quality Mode
# YYYYMMDD HHMMSS    SST Q M
# 20170101 000000 22.940 2 R
# 20170101 001000 22.908 2 R
# . . .
# 20170103 112000 22.180 2 R
# 20170103 113000 -9.999 9 R
# 20170103 114000 -9.999 9 R
# 20170103 115000 22.154 2 R
# . . .
# 20171103 233000 21.076 2 R
# 20171103 234000 21.055 2 R
# 20171103 235000 21.005 2 R
class ParserNOAA(Parser):
    def __init__(self):
        super(ParserNOAA, self).__init__()
        self.nodata = "-9.999"

    def _parse_header(self, line):
        s_line = line.split()
        parsing_header = True
        if s_line[0] == 'YYYYMMDD':
            self._parse_columns(s_line)
            parsing_header = False
        return parsing_header

    def process_data(self):
        self._post_parsing()
        super(ParserNOAA, self).process_data()

    def _post_parsing(self):
        column_names = self.df.columns.values
