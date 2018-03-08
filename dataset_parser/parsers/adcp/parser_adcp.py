from datetime import datetime
import numpy as np

from .. import parser_base


class ParserADCP(parser_base.ParserBase):
    NAME = "ADCP"

    def __init__(self, logger=None):
        super(ParserADCP, self).__init__()
        self.logger = logger
        self.nodata = "-99.999"
        self.date_format = "%Y%m%d %H%M%S"  # "20101127 020000"
        self.asc_timestamp = False

    # EXAMPLE:
    # Platform: T0N140W 2010-11-27 to 2016-04-05 (42261 total rows, 5 deployments) File Generated on 2018-02-17
    # Parameter(s): DEPTH ("m"), UCUR, VCUR, WCUR ("m/s"), -99.999 = missing
    # Deployment: CA016-20101127 2010-11-27 to 2011-08-23 (6461 data rows)
    # Remark: The following ASCII current profile data are interpolated to 5 meter depths and are not quality controlled.
    # Select NetCDF option to download velocity components U, V, W and quality control information
    # percent good, echo intensity, error velocity, as well as transducer head's pressure, pitch, roll, and heading data.
    # YYYYMMDD HHMMSS DEPTH    UCUR    VCUR    WCUR
    def _parse_header(self, line):
        s_line = line.split()
        if s_line[0] == "YYYYMMDD":
            self._parse_columns(s_line)
            self.parsing_header = False

    def _parse_columns(self, s_line):
        self.columns = s_line[2:]  # ['DEPTH', 'UCUR', 'VCUR', 'WCUR']
        self.columns_length = len(self.columns)

    # EXAMPLE:
    # 20101127 020000  10.0 -99.999 -99.999 -99.999
    # ...
    # 20101127 020000  45.0   0.199   0.329   0.002
    # ...
    # 20101127 020000  85.0   1.151   0.073   0.018
    def parse_data(self, line):
        s_line = line.split()
        try:
            date = s_line[0] + ' ' + s_line[1]
            timestamp = datetime.strptime(date, self.date_format)
            values = s_line[2:]
            data = [self._map_value(x) for x in values]
            return {'timestamp': timestamp, 'values': data}
        except:
            self.logger.info("INVALID LINE: %s", line.strip('\n'))
            return None

    def _map_value(self, value):
        return np.nan if value == self.nodata else float(value)

    # @staticmethod
    # def plot(path, filename, df):
    #     title = filename
    #     df = df.copy(deep=True)
    #     min_value, max_value = df.loc[df.idxmin()]['SST'][0], df.loc[df.idxmax()]['SST'][0]
    #     nan_value = min_value - (max_value - min_value) / 10
    #     df['SSTnan'] = df['SST']
    #     df['SSTnan'] = df['SSTnan'].apply(lambda x: nan_value if pd.isnull(x) else np.nan)
    #
    #     fig, ax = plt.subplots()
    #     df['SST'].plot(ax=ax, linestyle='none', title=title, marker='.', markersize=0.2)
    #     df['SSTnan'].plot(ax=ax, linestyle='none', marker='.', markersize=1)
    #     ax.legend()
    #     fig = ax.get_figure()
    #     fig.savefig(path + '/' + title + '.plot.png')
