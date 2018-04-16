from datetime import datetime
from .. import parser_base


class ParserNOAASPC(parser_base.ParserBase):
    NAME = "NOAA-SPC"

    #
    # dataset can be 'hail', 'tornado' or 'wind'
    #
    def __init__(self, logger, dataset):
        super(ParserNOAASPC, self).__init__()
        self.logger = logger
        self.nodata = "X"  # doesn't matter
        self.date_format = "%Y-%m-%d %H:%M:00+00:00"  # "2015-02-01 21:47:00+00:00"
        self.dataset = dataset
        self.name = self.NAME + "-" + self.dataset
        self.time_unit = "minutes"

    def _parse_header(self, _):
        self.columns = ['Latitude', 'Longitude']
        if self.dataset == 'hail':
            self.columns.append('Size')
        elif self.dataset == 'wind':
            self.columns.append('Speed')
        self.columns_length = len(self.columns)
        self.parsing_header = False

    def parse_data(self, line):
        timestamp = datetime.strptime(line[1], self.date_format)
        data = line[7:9]  # latitude and longitude
        data = [float(value)*100 for value in data]

        if self.dataset == 'hail':
            value = float(line[3])
            # int_value = int(value)
            # if int_value % 25 != 0:
            #     value = self._map_value(int_value)
            # value /= value
            data.append(value)
        elif self.dataset == 'wind':
            value = float(line[2])
            data.append(value)

        return {'timestamp': timestamp, 'values': data}

    # def _map_value(self, int_value):
    #     if int_value == 333:
    #         value = float(325)
    #     elif int_value == 113:
    #         value = float(125)
    #     elif int_value == 110:
    #         value = float(100)
    #     elif int_value == 115:
    #         value = float(125)
    #     elif int_value == 149:
    #         value = float(150)
    #     elif int_value == 112:
    #         value = float(100)
    #     elif int_value == 165:
    #         value = float(150)
    #     elif int_value == 311:
    #         value = float(300)
    #     elif int_value == 210:
    #         value = float(200)
    #     elif int_value == 217:
    #         value = float(225)
    #     elif int_value == 230:
    #         value = float(225)
    #     elif int_value == 269:
    #         value = float(275)
    #     elif int_value == 301:
    #         value = float(300)
    #     elif int_value == 102:
    #         value = float(100)
    #     else:
    #         raise StandardError("value must be a multiple of 25. value = %s" % int_value)
    #
    #     return value
