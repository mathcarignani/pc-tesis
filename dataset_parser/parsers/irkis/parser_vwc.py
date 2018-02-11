from datetime import datetime
import numpy as np

from .. import parser_base

        
class ParserVWC(parser_base.ParserBase):
    NAME = "IRKIS"

    def __init__(self):
        super(ParserVWC, self).__init__()
        self.nodata = "-999.000000"
        self.date_format = "%Y-%m-%dT%H:%M"  # "2009-10-01T01:00"

    # In the vwc files the header is only the first line.
    # EXAMPLE:
    # timestamp -10cm_A -30cm_A -50cm_A -80cm_A -120cm_A -10cm_B -30cm_B -50cm_B -80cm_B -120cm_B
    def _parse_header(self, line):
        s_line = line.split()
        self.columns = s_line[1:]
        self.columns_length = len(self.columns)
        self.parsing_header = False

    # EXAMPLE:
    # 2009-10-01T01:00  279.26   275.43   275.43    1.1     0    0.0      0      0 271.947  0.000    0.000   1.000
    def parse_data(self, line):
        s_line = line.split()
        timestamp = datetime.strptime(s_line[0], self.date_format)
        values = s_line[1:]
        if self.columns_length != len(values):
            raise StandardError("self.columns_length != len(data)")
        data = [self._map_value(x) for x in values]
        return {'timestamp': timestamp, 'values': data}

    def _map_value(self, value):
        return ParserVWC.NO_DATA if value == self.nodata else round(float(value)*1000, 0)

    @staticmethod
    def plot(path, filename, df):
        sensor_labels = ['A', 'B']
        for label in sensor_labels:
            label_columns = [col for col in df.columns if label in col]
            df_label = df[label_columns]  # remove columns from the other label
            ParserVWC.plot_non_nan(path, filename, df_label, label)
            ParserVWC.plot_nan(path, filename, df_label.copy(), label)

    @staticmethod
    def plot_non_nan(path, filename, df_label, label):
        title = 'Sensors with label ' + label + ' in ' + filename
        ax = df_label.plot(title=title, ylim=[0, 600])
        fig = ax.get_figure()
        fig.savefig(path + '/' + filename + '_' + label + '_data.png')

    @staticmethod
    def plot_nan(path, filename, df_label, label):
        title = 'Sensors with label ' + label + ' in ' + filename + ' (nans)'

        columns_len = len(df_label.columns)
        for idx, column in enumerate(df_label.columns):
            df_label.loc[df_label[column].notnull(), column] = -1  # replace all non-nan values by -1
            df_label.loc[df_label[column].isnull(), column] = idx + 1  # replace all nan values by columns_len - idx
            df_label.loc[df_label[column] == -1, column] = np.nan  # replace all -1 values by nan

        ax = df_label.plot(title=title, ylim=[0, columns_len + 1])
        fig = ax.get_figure()
        fig.savefig(path + '/' + filename + '_' + label + '_nan.png')