from datetime import datetime

from .. import parser_base

        
class ParserVWC(parser_base.ParserBase):
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
