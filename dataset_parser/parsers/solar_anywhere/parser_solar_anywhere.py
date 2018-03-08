from datetime import datetime
import numpy as np

from .. import parser_base


class ParserSolarAnywhere(parser_base.ParserBase):
    NAME = "SolarAnywhere"

    def __init__(self, logger):
        super(ParserSolarAnywhere, self).__init__()
        self.logger = logger
        self.nodata = "NaN"
        self.date_format = "%m/%d/%Y %H:%M"  # "06/14/2013 17:00"
        self.columns = ['GHI', 'DNI', 'DHI']
        self.columns_length = len(self.columns)

    def _parse_header(self, line):
        if line[0] == "Date (MM/DD/YYYY)":
            self.parsing_header = False

    def parse_data(self, line):
        try:
            date = line[0] + ' ' + line[1]
            timestamp = datetime.strptime(date, self.date_format)
            values = [line[4], line[7], line[10]]  # GNI, DNI, DHI
            data = [self._map_value(x) for x in values]
            return {'timestamp': timestamp, 'values': data}
        except:
            self.logger.info("INVALID LINE: %s", ' '.join(line))
            return None

    def _map_value(self, value):
        return ParserSolarAnywhere.NO_DATA if value == self.nodata else float(value)

    @staticmethod
    def plot(path, filename, df):
        ParserSolarAnywhere.plot_non_nan(path, filename, df)
        ParserSolarAnywhere.plot_each(path, filename, df)
        ParserSolarAnywhere.plot_nan(path, filename, df)

    @staticmethod
    def plot_non_nan(path, filename, df):
        title = filename + ' (data)'
        ax = df.plot(title=title, ylim=[0, 1100])
        fig = ax.get_figure()
        fig.savefig(path + '/' + filename + '_data.png')

    @staticmethod
    def plot_each(path, filename, df):
        colors = {'GHI': 'Blue', 'DNI': 'Orange', 'DHI': 'Green'}
        for column in df.columns:
            title = filename + ' ' + column
            column_key = column[-3:]  # "0_0_GHI" => "GHI"
            ax = df[[column]].plot(title=title, ylim=[0, 1100], color=colors[column_key])
            fig = ax.get_figure()
            fig.savefig(path + '/' + filename + '_' + column + '.png')

    @staticmethod
    def plot_nan(path, filename, df):
        title = filename + ' (nan)'

        columns_len = len(df.columns)
        for idx, column in enumerate(df.columns):
            df.loc[df[column].notnull(), column] = -1  # replace all non-nan values by -1
            df.loc[df[column].isnull(), column] = idx + 1  # replace all nan values by columns_len - idx
            df.loc[df[column] == -1, column] = np.nan  # replace all -1 values by nan

        ax = df.plot(title=title, ylim=[0, columns_len + 1])
        fig = ax.get_figure()
        fig.savefig(path + '/' + filename + '_nan.png')
