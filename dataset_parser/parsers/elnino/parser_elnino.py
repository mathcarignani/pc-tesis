from datetime import datetime

from .. import parser_base


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
    NAME = "EL-NINO"

    def __init__(self):
        super(ParserElNino, self).__init__()
        self.nodata = "."
        self.date_format = "%Y%m%dT%H:%M"  # "19981001T00:00"
        self.asc_timestamp = False
        self._parse_header(None)

    # EXAMPLE
    # obs - year - month - day - date - lat - long - zon.winds - mer.winds - humidity - air temp. - s.s.temp.
    def _parse_header(self, _):
        self.columns = ['lat', 'long', 'zon.winds', 'mer.winds', 'humidity', 'air.temp', 'ss.temp']
        self.columns_length = len(self.columns)
        self.parsing_header = False

    def parse_data(self, line):
        # 2 80 3 8 800308 -0.02 -109.46 -4.9 1.1 . 25.66 25.97
        s_line = line.split()
        timestamp = datetime.strptime("19" + s_line[4] + "T00:00", self.date_format)

        values = s_line[5:]
        if self.columns_length != len(values):
            raise StandardError("self.columns_length != len(data)")

        # lat, long, zon_winds, mer_winds, humidity, air_temp, ss_temp = values

        data = [self._map_value(x) for x in values]
        return {'timestamp': timestamp, 'values': data}

    def _map_value(self, value):
        return ParserElNino.NO_DATA if value == self.nodata else float(value)

    @staticmethod
    def plot(path, filename, df):
        pass
