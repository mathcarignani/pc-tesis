from datetime import datetime

from .. import parser_base


class ParserClimaps(parser_base.ParserBase):
    NAME = "Climaps"

    def __init__(self):
        super(ParserClimaps, self).__init__()
        self.nodata = "TODO"
        self.date_format = "%Y-%m-%dT%H:%M:00Z"  # "2018-01-01T00:00:00Z"
        self.columns = []
        self.hash_counter = 0

    def _parse_header(self, line):
        if "MeasurementId" in line[0]:
            column_name = line[3].replace(" Measurement = ", "")
            self.columns.append(column_name)
        elif line[0] == "#":
            self.hash_counter += 1
            if self.hash_counter == 2:
                self.parsing_header = False
                self.columns_length = len(self.columns)

    def parse_data(self, line):
        timestamp = datetime.strptime(line[0][1:], self.date_format)
        values = line[1:]
        data = [self._map_value(x) for x in values]
        return {'timestamp': timestamp, 'values': data}

    def _map_value(self, value):
        return ParserClimaps.NO_DATA if value == self.nodata else float(value)

    @staticmethod
    def plot(path, filename, df):
        for column in df.columns:
            ParserClimaps.plot_column(path, filename, df, column)

    @staticmethod
    def plot_column(path, filename, df, column):
        title = filename + " (" + column + ")"
        ax = df[[column]].plot(title=title)
        fig = ax.get_figure()
        fig.savefig(path + '/' + filename + '_' + column.replace(" ", "_") + '.png')
