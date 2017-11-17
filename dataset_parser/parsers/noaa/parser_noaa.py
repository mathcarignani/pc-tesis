from .. import parser_base
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
class ParserNOAA(parser_base.ParserBase):
    def __init__(self):
        super(ParserNOAA, self).__init__()
        self.nodata = "-9.999"

    def _parse_header(self, line):
        s_line = line.split()
        parsing_header = True
        if s_line[0] == "YYYYMMDD":
            self._parse_columns(s_line)
            parsing_header = False
        return parsing_header

    def _parse_columns(self, s_line):
        # EXAMPLE:
        # YYYYMMDD HHMMSS    SST Q M
        self.df = pd.DataFrame(columns=[s_line[2]])
        self.columns_count = len(self.df.columns)

    def _parse_data(self, line):
        # 20170101 000000 22.940 2 R
        s_line = line.split()

        try:
            date = s_line[0] + ' ' + s_line[1]
            timestamp = pd.to_datetime(date, format='%Y%m%d %H%M%S')
            data = np.array([s_line[2]])
            np_array = self._clean_data(data)
            self.df.loc[timestamp] = np_array
        except:
            self.errors['errors'].append(line)

    def plot(self, filename):
        title = filename
        df = self.df.copy(deep=True)
        min_value = df.loc[df.idxmin()]['SST'][0]
        max_value = df.loc[df.idxmax()]['SST'][0]
        df['SSTnan'] = df['SST']
        nan_value = min_value - (max_value - min_value) / 10
        df['SSTnan'] = df['SSTnan'].apply(lambda x: nan_value if pd.isnull(x) else np.nan)

        fig, ax = plt.subplots()
        df['SST'].plot(ax=ax, linestyle='none', title=title, marker='.', markersize=0.2)
        df['SSTnan'].plot(ax=ax, linestyle='none', marker='.', markersize=1)
        ax.legend()
        fig = ax.get_figure()
        fig.savefig(title + '.plot.png')
