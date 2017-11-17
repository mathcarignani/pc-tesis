from .. import parser_base
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 1 80 3 7 800307 -0.02 -109.46 -6.8 0.7 . 26.14 26.24
# 2 80 3 8 800308 -0.02 -109.46 -4.9 1.1 . 25.66 25.97
# 3 80 3 9 800309 -0.02 -109.46 -4.5 2.2 . 25.69 25.28
# 4 80 3 10 800310 -0.02 -109.46 -3.8 1.9 . 25.57 24.31
# 5 80 3 11 800311 -0.02 -109.46 -4.2 1.5 . 25.3 23.19
# 6 80 3 12 800312 -0.02 -109.46 -4.4 0.3 . 24.72 23.64
# 7 80 3 13 800313 -0.02 -109.46 -3.2 0.1 . 24.66 24.34
# . . .
# 178077 98 6 12 980612 8.96 -140.32 -4.3 -3.3 93.2 25.8 27.87
# 178078 98 6 13 980613 8.95 -140.34 -6.1 -4.8 81.3 27.17 27.93
# 178079 98 6 14 980614 8.96 -140.33 -4.9 -2.3 76.2 27.36 28.03
# 178080 98 6 15 980615 8.95 -140.33 . . . 27.09 28.09
class ParserElNino(parser_base.ParserBase):
    def __init__(self):
        super(ParserElNino, self).__init__()
        self._parse_header(None)
        self.parsing_header = False
        self.nodata = "."

    def _parse_header(self, _):
        self._parse_columns(_)

    def _parse_columns(self, s_line):
        # EXAMPLE
        # obs - year - month - day - date - lat - long - zon.winds - mer.winds - humidity - air temp. - s.s.temp.
        columns = ['date', 'lat', 'long', 'zon.winds', 'mer.winds', 'humidity', 'air.temp', 'ss.temp']
        self.df = pd.DataFrame(columns=columns)
        self.columns_count = len(self.df.columns)

    def _parse_data(self, line):
        # 2 80 3 8 800308 -0.02 -109.46 -4.9 1.1 . 25.66 25.97
        s_line = line.split()

        try:
            np_array = None
            current_date = '19' + s_line[4]
            timestamp = pd.to_datetime(current_date, format='%Y%m%d')
            data = s_line[4:]
            self._add_data(data, current_date, line, timestamp, np_array)
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
