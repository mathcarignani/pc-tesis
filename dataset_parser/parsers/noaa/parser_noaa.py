from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .. import parser_base


class ParserNOAA(parser_base.ParserBase):
    NAME = "NOAA"

    def __init__(self, logger):
        super(ParserNOAA, self).__init__()
        self.logger = logger
        self.nodata = "-9.999"
        self.date_format = "%Y%m%d %H%M%S"  # "20170103 113000"

    # EXAMPLE:
    # Platform: T0N95W 2017-01-01 to 2017-11-03 (31142 total rows, 2 deployments) File Generated on 2017-11-05
    # Parameter(s): Sea Surface Temperature ("degree celsius"), -9.999 = missing
    # Deployment: DM179A-20160312 2017-01-01 to 2017-03-27 (11995 data rows, 1 depth columns)
    # Depth (Meters)       1 Quality Mode
    # YYYYMMDD HHMMSS    SST Q M
    def _parse_header(self, line):
        s_line = line.split()
        if s_line[0] == "YYYYMMDD":
            self._parse_columns(s_line)
            self.parsing_header = False

    def _parse_columns(self, s_line):
        self.columns = [s_line[2]]  # only select SST
        self.columns_length = len(self.columns)

    # EXAMPLE:
    # 20170101 000000 22.940 2 R
    # ...
    # 20170103 113000 -9.999 9 R
    # ...
    # 20170103 115000 22.154 2 R
    def parse_data(self, line):
        s_line = line.split()
        try:
            date = s_line[0] + ' ' + s_line[1]
            timestamp = datetime.strptime(date, self.date_format)
            values = [s_line[2]]  # only select SST
            data = [self._map_value(x) for x in values]
            return {'timestamp': timestamp, 'values': data}
        except:
            self.logger.info("INVALID LINE: %s", line.strip('\n'))
            return None

    def _map_value(self, value):
        return np.nan if value == self.nodata else float(value)

    @staticmethod
    def plot(path, filename, df):
        title = filename
        df = df.copy(deep=True)
        min_value, max_value = df.loc[df.idxmin()]['SST'][0], df.loc[df.idxmax()]['SST'][0]
        nan_value = min_value - (max_value - min_value) / 10
        df['SSTnan'] = df['SST']
        df['SSTnan'] = df['SSTnan'].apply(lambda x: nan_value if pd.isnull(x) else np.nan)

        fig, ax = plt.subplots()
        df['SST'].plot(ax=ax, linestyle='none', title=title, marker='.', markersize=0.2)
        df['SSTnan'].plot(ax=ax, linestyle='none', marker='.', markersize=1)
        ax.legend()
        fig = ax.get_figure()
        fig.savefig(path + '/' + title + '.plot.png')

    ####################################################################################################################

    BITS = 16
    DELTA = "00:10:00"
    NONE = 40001

    @classmethod
    def csv_to_alphabet(cls, x):
        if x == 'N':
            return cls.NONE
        elif 0 <= int(x) <= 40000:
            return int(x)
        else:
            raise StandardError("Invalid value in the csv", x)

    @classmethod
    def alphabet_to_csv(cls, y):
        if y == cls.NONE:
            return 'N'
        elif 0 <= y <= 40000:
            return y
        else:
            raise StandardError("Invalid value in the alphabet", y)

    @classmethod
    def check_delta(cls, delta_str):
        pass
