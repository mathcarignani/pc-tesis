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

        lat, long, zon_winds, mer_winds, humidity, air_temp, ss_temp = values
        zon_winds, mer_winds, humidity = [self._check_commas(x, 1) for x in [zon_winds, mer_winds, humidity]]
        lat, long, air_temp, ss_temp = [self._check_commas(x, 2) for x in [lat, long, air_temp, ss_temp]]
        data = [lat, long, zon_winds, mer_winds, humidity, air_temp, ss_temp]

        return {'timestamp': timestamp, 'values': data}

    #
    # Check that the value doesn't have more numbers after the comma than its supposed to
    #
    def _check_commas(self, value, power):
        if value == self.nodata:
            return ParserElNino.NO_DATA

        split_value = value.split(".")
        if len(split_value) == 2 and len(split_value[1]) > power:
            raise StandardError("More than power (%s) numbers after the comma. value = %" % (power, value))

        return float(value) * 10 ** power


    @staticmethod
    def plot(path, filename, df):
        pass
